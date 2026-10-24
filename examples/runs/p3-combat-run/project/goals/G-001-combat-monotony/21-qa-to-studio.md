---
kind: handoff
goal: G-001
seq: 21
from: qa
to: studio
stage: Verify
outcome: question
---
# 21: qa → studio — Verification of the dash/hit invulnerability fix in build 0.4: no verdict yet, because dash-during-hit-stun (D-003) cannot be observed

## Task

Get the build description for dash and attack presses during hit-stun brought in line with D-003, then re-route to QA for a final verdict. Everything else the build describes meets the acceptance criteria. I cannot give `pass` while one part of criteria 2 and 5 is unobservable. I am not giving `fail` either, because nothing observed contradicts the spec.

## Context

Goal G-001 (combat monotony). Handoff 10 was blocked because no build was in the packet. This time `sim/build-0.4.md` (latest) and `sim/build-0.3.md` (baseline) were supplied. I verified from those two files, `design/combat.md`, D-001, D-003 and the criteria in `05-qa-to-studio.md`.

## Findings

### Nature of the evidence

Both builds are player-observable descriptions. There are no recordings or logs, and no per-run counts. My evidence is what `sim/build-0.4.md` states, quoted below. I did not use the "why it works" explanation in handoff 12.

- The 0.4 file's heading says "build 0.3.1", but the file is `build-0.4.md`. I treated it as the latest build, as the handoff says.
- `build-0.3.md` states only "Occasionally, if you dash right after being hit, you take damage partway through the dash." It gives no timings. The baseline comparison is therefore qualitative: 0.3 had the defect, and 0.4 states the following.
  - It gives no damage during the dash, for every start time after hit-stun.
  - Protection lasts to at least 0.8 s after the hit.

### Per-criterion results

The 0.4 description states that behavior is the same at 30 and 60 FPS, except for the exact frame at which an edge lands. It gives no separate per-frame-rate observations, so the 30 and 60 columns carry the same evidence.

| # | Criterion | 30 FPS | 60 FPS | Evidence (0.4) |
|---|---|---|---|---|
| 1 | Earliest dash (~0.3 s after hit): no damage in the 0.25 s dash; 20+ repeats; Grub and Spitter | consistent with pass | consistent with pass | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after the dash ends. You stay protected until 0.8 s after the hit." "Holds for Grub contact and Spitter projectiles alike." Repeat count of 20: not demonstrable from a description. |
| 2 | Varied delays, including hit-stun, just before, at and after 0.8 s: no damage in an active dash | **part unobservable** | **part unobservable** | 0.3–0.55 s and 0.55–<0.8 s: no damage mid-dash ("Damage cannot land partway through the dash"). At or after 0.8 s: "the dash gives its own 0.25 s of protection." Dash pressed during hit-stun: "behaves as it did in 0.3." `build-0.3.md` does not describe that case, so it is unobservable (see Gap below). |
| 3 | Directions (towards and away), rooms 1–5, Grubs and Spitters | consistent with pass | consistent with pass | "Holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source." Rooms 1–5 are not named per case; the build says there are "no other changes to enemies, rooms or attacks." |
| 4 | Dash with no preceding hit: full 0.25 s invulnerability | pass | pass | "you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends." |
| 5 | Existing rules: hit-stun 0.3 s no input, hit invulnerability to 0.8 s, cooldown 0.6 s, attack queued in dash fires at end | **hit-stun input part unobservable**; rest pass | same | "Stunned with no input for the first 0.3 s"; "cannot be damaged for 0.8 s after the hit"; "0.6 s dash cooldown are unchanged"; "An attack pressed during a dash still fires when the dash ends." The build does not state whether a dash or attack press during hit-stun is ignored (D-003) or buffered. |
| 6 | Mid-dash damage is not deferred to just after the dash; damage after the windows is normal | consistent with pass | consistent with pass | Protection continues after the dash to 0.8 s after the hit, and damage "can land again" only after that. Nothing describes damage being stored and released. This is thin evidence. A real run should confirm that nothing lands in the frame after the dash ends. |

### Boundary results (frame length in view)

- Dash end at 0.25 s: a damage event exactly on 0.25 s counts as after protection.
- Hit protection end at 0.8 s: a damage event exactly on 0.8 s counts as after protection.
- A dash pressed at 0.8 s or later gets its own full 0.25 s.
- Frame length is about 33 ms at 30 FPS and about 17 ms at 60 FPS. Per the build, an edge event can differ by one frame between the two rates.
- That is at most about 33 ms at 30 FPS and about 17 ms at 60 FPS. Nothing in the description shows a difference larger than one frame, and nothing is hidden by the tolerance.
- The description gives no measured timestamps at 0.79, 0.8 or 0.85 s, only the rules above. Those are the rules I checked against.

### Regressions checked

- Dash distance, duration and cooldown: unchanged per the build.
- Attack queued during a dash: unchanged per the build.
- Enemies, rooms and attacks: unchanged per the build.
- Flicker and sound cues: the build does not describe them, so they are not verified.

### Gap (blocking the verdict)

`design/combat.md` and D-003 are clear: input during hit-stun, dash and attack alike, is ignored, not buffered. `sim/build-0.4.md` says only that a dash pressed during hit-stun "behaves as it did in 0.3." `sim/build-0.3.md` does not describe that behavior. So the build offers no observation that it is ignored. Inferring it from "stunned with no input" would be inference from intent, which my instructions rule out. The expected behavior is not a spec gap. The gap is in what the build shows.

Nothing observed contradicts any criterion, so I record no failure.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input.
- D-003: Input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from the spec, criteria and build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- Do not count the fix as verified until the hit-stun input behavior is observable.

## Open questions

1. Please get `sim/build-0.4.md` (or its successor) to state the observable behavior for a dash press and an attack press during the 0.3 s hit-stun. D-003 expects that the press does nothing, does not fire at the end of hit-stun, and does not start the dash. The requested wording should cover both the dash and the attack.
2. Optional, for a fuller verdict: observed per-frame-rate results at 30 and 60 FPS for the 20 repeats in criterion 1, and a statement of what happens in the frame right after a dash ends while a damage source is still in contact (criterion 6).

## Expected output

Studio asks `gameplay-engineer` to update the build description with the hit-stun input behavior (open question 1). Studio then re-routes to `qa`, with the new build and this handoff in the Load. QA will then return `pass` or `fail`. If everything else holds and the hit-stun behavior is ignored, the verdict will be `pass`. If a press during hit-stun is buffered or starts a dash, the verdict will be `fail` against D-003 and the criteria.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
