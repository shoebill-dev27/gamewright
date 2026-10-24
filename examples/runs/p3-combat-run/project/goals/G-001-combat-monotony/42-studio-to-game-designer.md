---
kind: handoff
goal: G-001
seq: 42
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 42: studio → game-designer — Settle how Phase 1 criteria 1 and 2 are judged in this dry run, and answer QA's design items D1–D6

## Task

Decide how acceptance criteria 1 and 2 (Phase 1 part) of `design/g001-combat-escalation.md` are to be judged when no counted run can exist, and answer QA's design items D2–D6 (D1 is covered by the first question). Amend the spec and D-008 where your answers change them. Address the result to `studio`.

## Context

G-001, Phase 1 (encounter escalation, D-002, D-008). `qa` verified the Phase 1 build (`sim/build-0.6.md`) against the amended spec. Result: criteria 3, 4, 5 and 10 pass at 30 and 60 FPS, judged from the build's stated behavior. The regression check against `sim/build-0.5.md` found no change. Criteria 1 and 2 (Phase 1 part) are `question`: they ask for counted results, and the build is a description that has none.

This project is a dry run (`project.md#constraints`): "running the build" means reading `sim/build-0.6.md`. The Studio does not decide verification scope or acceptance criteria. Those belong to you (criteria in your spec) and to `qa` (verdicts). QA named the exact missing input and asked who decides how these two criteria are judged.

## Findings

QA's report is handoff 40, which is in your Load list. It is the authority for the details below.

Verdicts (same at 30 and 60 FPS):

- Criterion 1 (rooms 4–5 not clearable by holding one position: at least 4 of 5 attempts per position take at least 2 hits or die): `question`. Missing input: for rooms 4 and 5, for each of the 5 positions (4 corners, centre), at least 5 scripted attempts (facing the nearest spawn side, attacking only), with hits taken and death per attempt. The build says only that hits "depend on the room size and speeds, which are not stated here".
- Criterion 2, Phase 1 part (a dash taken in combat in at least 3 of 5 rooms): `question`. Missing input: for rooms 1–5, whether a dash was taken in combat in a played or scripted run. The build says dash is "available as before" and says nothing about use.
- Criteria 3, 4, 5, 10: pass, with the limits QA lists.
- Existing values (spec 3.8: Grub, player and projectile speed, projectile range, hearts, room size, hitbox sizes): "not shown". You waived them in handoff 35 (D-008), so criterion 1 cannot be judged by calculation either.

QA's design items:

- **D1** The existing values are not shown. Whether criterion 1 can be judged by calculation instead of counts depends on them.
- **D2** Criterion 5 requires identical points "exactly". The sampling rule (the player position is read on the next logic frame after a between-frame ring start) can give different points at 30 and 60 FPS for a moving player close to a threshold: the 5-tile test, or the 1.5-tile occupancy test against a moving Grub. Decide whether scripts must keep clear of thresholds, or whether the rule needs a frame-rate-independent sampling time.
- **D3** Criterion 4 says the Spitter's first shot is at least 1.0 s after appearing, with no tolerance. Criterion 5 allows ±1 frame on shot times. If `appearTime` is the scheduled time, the first shot can come less than one frame short of 1.0 s after the first visible frame at 30 FPS. State which governs.
- **D4** Spec 3.3, when no candidate passes both tests: "take the candidate that is not occupied and farthest". The build's wording covers two cases (no point far enough; every point occupied) but not the mixed case (one point near and free, another far but occupied). State the intended result so that a verifier can check it. QA did not verify this case.
- **D5** Room 2 wave 2 Grub list E3, E1, E2: E1 and E3 are 0.25H from E2, where the wave 1 Spitter stands. If room height H is 6 tiles or less and that Spitter is alive, all three points are occupied and the farthest-overall fallback is always used. The same applies to the Spitter's far-end alternative if the wall is shorter than about 6.5 tiles. Decide whether this needs a minimum room size or a changed list, or whether it is accepted and reported via the `SPAWN_FALLBACK` path in 3.8 and D-008 "Revisit when". QA could not give the `SPAWN_FALLBACK` count.
- **D6** Criterion 2 (Phase 1) counts "a dash taken in combat". A script can satisfy it by dashing regardless of need. State whether the check is meant to show need, or whether it is a playtest signal only.

## Decisions already made

- D-001: one-button combat; no new input.
- D-002: encounter escalation (Phase 1) first, then behavior variants (Phase 2) if combat is still monotonous.
- D-004: gameplay numbers are data; timers are timestamps on the game clock.
- D-008: Phase 1 spawn and wave rules.

## Constraints

- No pillar, input, scope or Owner Decision may change. If your answer needs one of these, say so and hand back (`game-director`, or the Studio for an Owner escalation).
- Keep the intent of criteria 1 and 2: Phase 1 should remove the "one position wins" stance and give the player a reason to dash. If you change how they are judged, say which evidence source replaces the counted run and what that source must record (for example, items the playtester records without being told the expected result). Do not just lower thresholds without a reason.
- If your answers change what Build must do (for example D2 or D4 need a rule change in the build), state it exactly. The Studio then opens a narrow Build and a re-Verify.
- Phase 2 content is out of scope.
- If the only way forward is information that no Role can produce, or a choice that depends on the Owner's taste, say so and name the input. The Studio then escalates.

## Open questions

The six items above. For D1, D2 and D6 you may answer "playtest signal only" or "deferred to playtest" if you give the reason and what must be recorded.

## Expected output

An amended `design/g001-combat-escalation.md` (and a Decision if an answer constrains later work, for example a judgement basis for criteria 1 and 2) and a handoff addressed to `studio` that:

1. states, for criteria 1 and 2 (Phase 1), the judging basis and who gives the verdict (`qa` on a build description, `playtester` observations, or a mix);
2. answers D2–D6 one by one;
3. says whether any Build change follows, and whether QA must re-verify anything.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; sim/build-0.6.md
- Decisions: decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/40-qa-to-studio.md
