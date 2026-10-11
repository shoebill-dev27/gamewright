---
kind: handoff
goal: G-001
seq: 31
from: qa
to: studio
stage: Verify
outcome: pass
---
# 31: qa → studio — Verification of the dash-damage fix (incl. hit-stun input) against build 0.5: criteria 1–6 pass, overall pass

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` (D-007). Give a verdict for criteria 1–6 and an overall verdict. The criteria wording is taken from handoff 05 (it governs). Handoff 23 supplies the numbering.

**Overall verdict: pass.** All six criteria pass at 30 FPS and 60 FPS. The only differences between the two frame rates are the one-frame edge differences that the build and the spec allow.

## Context

- Build under verification: `sim/build-0.5.md`. Baseline for the regression check: `sim/build-0.3.md`. `sim/build-0.4.md` was not used.
- The criteria text is now available, so this closes the question left open in handoff 29. Nothing is missing, and no criterion is unclear.
- Handoff 05 and handoff 23 agree. Handoff 23 characterises criteria 1 and 2 as dash protection, criterion 5 as hit-stun with no input, and criterion 6 as the frame after a dash ends. That matches the wording in 05. I found no disagreement to report.
- The build is a player-observable description, not a runnable build. Each verdict below rests on what the description states. The description says its statements hold "same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs".

## Findings

### Per-criterion verdicts (wording from handoff 05)

| # | Criterion (short) | Verdict | Evidence in `sim/build-0.5.md` |
|---|---|---|---|
| 1 | Dash at the earliest accepted moment (0.3 s after a hit): no damage during the 0.25 s dash, with a Grub in contact or a projectile arriving mid-dash. At least 20 repeats per frame rate with no damage. | PASS | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after it ends. You stay protected until 0.8 s after the hit." "A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected." "This holds for Grub contact and Spitter projectiles alike." The 0.3 baseline line "Occasionally … you take damage partway through the dash" is gone. The description states the behavior unconditionally, with no "occasionally" qualifier. |
| 2 | Dash presses at several delays after the hit, including early (during hit-stun) and just before, at and just after 0.8 s: no damage during any active dash. | PASS | Presses at about 0.05, 0.15 and 0.28 s start no dash, so no active dash exists to be damaged. This is consistent with D-003. Dashes started at 0.3–0.55 s and at 0.55 s to just under 0.8 s: no damage during the dash. Protection lasts through the later of the dash end and 0.8 s. A dash started at 0.8 s or later gets its own 0.25 s of protection. An event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection, and may differ by one frame between 30 and 60 FPS. That is allowed. |
| 3 | Different dash directions (toward and away from the source), rooms 1–5, Grubs and Spitters. | PASS | "This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source." The description gives no room-specific exception for rooms 1–5. |
| 4 | A dash with no preceding hit still gives full 0.25 s invulnerability (no regression). | PASS | "Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash." |
| 5 | Existing rules hold: hit-stun 0.3 s with no input; hit invulnerability until 0.8 s; dash cooldown 0.6 s; an attack pressed during a dash fires when the dash ends. | PASS | Stun: "You are stunned for the first 0.3 s", and dash and attack presses in that window do nothing. This matches D-003: nothing is buffered, held buttons do not fire, a fresh press works, and a hit cancels any waiting request. Hit invulnerability: "you cannot be damaged for 0.8 s after the hit". Cooldown: "the 0.6 s dash cooldown [is] unchanged". Attack queue: "If a swipe was pressed during a dash, it still fires when the dash ends." |
| 6 | Damage previously taken mid-dash is not delayed to land right after the dash ends. A hit landing after the invulnerability windows expire is normal. | PASS | After a hit, a dash is covered through the later of the dash end and 0.8 s, so nothing lands at the dash end while hit protection is active. With no preceding hit, "damage can land immediately after it ends". This is the normal case the criterion allows, because both windows have expired. The boundary frame counts as after protection and may differ by one frame between frame rates. Limit of this evidence: the description does not say outright that damage is not stored during a dash. It says only that no damage lands during the dash, and that damage afterwards follows the normal rules. I judged that sufficient for criterion 6 as worded. |

### Hit-stun input (the new part of criteria 2 and 5), re-checked against the criteria text

All six statements from handoff 28 are stated in the build and match D-003:
1. A dash press in hit-stun starts no dash and no cooldown.
2. An attack press in hit-stun gives no swipe, and nothing fires later.
3. Nothing fires at the end of the stun.
4. A held button does not fire. Release and re-press works.
5. Presses after 0.3 s work normally. A press exactly on the 0.3 s edge may differ by one frame between 30 and 60 FPS.
6. The hit-stun length is the same at 30 and 60 FPS.

Criterion 2 in handoff 05 was written before D-003. It lists "pressed early, during hit-stun" as a delay to test. Under D-003 such a press starts no dash, so the criterion's condition ("no damage during an active dash") holds because no dash exists. This is not a spec conflict.

### Conditions and limits

- **Frame rates:** the description states identical behavior at 30 and 60 FPS, apart from the exact edge frame. The only differences are the allowed one-frame boundary differences (0.3 s, 0.25 s and 0.8 s edges).
- **"At least 20 repeats per frame rate" (criteria 1 and 2):** the build is a description, so I could not actually repeat the dash 20 times. I judged against the unconditional statements above. If the Studio wants a counted run, it needs a runnable build.

### Regression check against `sim/build-0.3.md`

- Rooms 1–5, enemy behavior, the "hold position and swipe" pattern, and the rarely needed dash read the same as in 0.3. This is expected, because Phase 1 is not built yet.
- Dash distance, dash duration (0.25 s), the 0.6 s cooldown, and enemies, rooms and attacks are stated as unchanged.
- The only intended difference from 0.3 is the removal of the "occasionally take damage partway through the dash" line.
- No regression found.

### Optional notes

- **Frame right after a dash ends with a source in contact:** with no preceding hit, damage can land on that frame. After a hit, protection continues to the later of the dash end and 0.8 s. The boundary frame counts as after protection and may differ by one frame between 30 and 60 FPS, which is allowed.
- **Naming mismatch:** the file is `sim/build-0.5.md` but its heading reads "Simulated build 0.3.2". This is a labeling issue only. I treated the file as build 0.5 per D-007.
- **Invulnerability flicker and sound cues:** none described, not checked.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered. Build 0.5 matches it.
- D-007: verify against `sim/build-0.5.md`. I did.

## Constraints

- I did not widen or narrow the criteria. I did not modify the build.
- The verdict is limited to what the description states, as noted under "Conditions and limits".

## Open questions

None. The wording of criteria 1–6 was sufficient for a verdict on each. The loop-limit escalation to the Owner is not needed.

## Expected output

For `studio`: record the dash-damage fix, including the hit-stun input change, as verified (pass). Phase 1 of the chosen direction may proceed.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/30-studio-to-qa.md
