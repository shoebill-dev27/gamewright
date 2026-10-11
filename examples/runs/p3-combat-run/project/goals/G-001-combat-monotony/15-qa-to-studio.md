---
kind: handoff
goal: G-001
seq: 15
from: qa
to: studio
stage: Verify
outcome: question
---
# 15: qa → studio — Dash/hit invulnerability fix: build 0.4 matches most criteria, but dash-in-hit-stun cannot be judged, so no pass

## Task

Route a request to `gameplay-engineer` (via Studio) to make the hit-stun dash behavior in `sim/build-0.4.md` observable and consistent with D-003. Then re-route verification to QA. This step gives no `pass` or `fail`, because one required case cannot be judged from the build.

## Context

Goal G-001 (combat monotony). Handoff 12 asked QA to verify the fix against the six criteria in `05-qa-to-studio.md` at 30 and 60 FPS. This time the build files were supplied (`sim/build-0.4.md`, baseline `sim/build-0.3.md`). The handoff says criterion 2 and 5 must cover a dash pressed during hit-stun, now specified by D-003 as ignored.

## Findings

### Verdict

No verdict. **Blocked on one case.** Nothing observed fails. A `pass` requires every criterion to pass, and one cannot be judged.

### The blocker

`sim/build-0.4.md` says only this about a dash pressed during hit-stun: "behaves as it did in 0.3." `sim/build-0.3.md` does not describe that behavior either. So neither build states whether the press is ignored, buffered or something else. D-003 requires "ignored, not buffered", and the build gives no observation to compare with it. Inferring "ignored" from "same as 0.3" would be inventing evidence. The spec is defined, so this is not a spec gap for `game-designer`. It is a build-observability gap.

### Other limits of the evidence

- The build files are player-observable prose, not run data. They give no repeat counts (criterion 1 needs at least 20 per frame rate) and no measured boundary results. They do not list rooms 1–5 individually. I cannot record "20 of 20 clean" or measured 0.8 s / 0.85 s results with the frame lengths (about 33 ms and 17 ms) in view. I can only compare what the description states against the criteria.
- `sim/build-0.4.md` has the heading "Simulated build 0.3.1". Its file name is 0.4. I assume they are the same build, but please confirm.

### Per-criterion comparison with `sim/build-0.4.md`

The build says its behavior is the same at 30 and 60 FPS, apart from which frame an edge lands on. The 30 and 60 FPS columns are therefore identical, and neither is an independently observed run.

| # | Criterion | 30 FPS | 60 FPS | Evidence (build 0.4 text) |
|---|---|---|---|---|
| 1 | Earliest dash (~0.3 s after hit): no damage in the 0.25 s dash, ≥20 repeats, Grub and Spitter | consistent; repeats not demonstrated | consistent; repeats not demonstrated | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after… until 0.8 s"; holds for "Grub contact and Spitter projectiles alike". 0.3 had "Occasionally… you take damage partway through the dash"; 0.4 has no such line. |
| 2 | Varied delays: in hit-stun, just before, at and after 0.8 s | **not judgeable for hit-stun**; the other delays are consistent | **not judgeable for hit-stun**; the other delays are consistent | 0.3–0.55 s, 0.55–<0.8 s and ≥0.8 s are each described with no damage during the dash. The hit-stun press is "as it did in 0.3", which is not described. Boundary: a hit exactly on 0.8 s or 0.25 s counts as after protection, and "can differ by one frame". |
| 3 | Directions, rooms 1–5, Grubs and Spitters | consistent; per-room runs not shown | consistent; per-room runs not shown | "toward or away from the damage source"; Grub and Spitter named. Rooms are not mentioned in the dash text, and there are no other room changes. |
| 4 | Dash with no hit: full 0.25 s protection | consistent | consistent | "you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends." |
| 5 | Existing rules: hit-stun 0.3 s with no input, hit invulnerability to 0.8 s, cooldown 0.6 s, attack queued in a dash fires at its end | partly consistent; hit-stun dash press not judgeable | partly consistent; hit-stun dash press not judgeable | Hit-stun 0.3 s with no input and protection to 0.8 s: stated. Cooldown "unchanged" at 0.6 s. Queued attack "still fires when the dash ends". The hit-stun press is undescribed (see blocker). |
| 6 | Mid-dash damage not delayed to land right after the dash; later damage normal | consistent; not observed directly | consistent; not observed directly | "Damage cannot land partway through the dash." After protection ends, damage lands normally. The text says nothing about damage being held or delayed. |

### Independence of the timers

This matches the `design/combat.md` clarification and D-003. 0.4 gives protection through the later of the dash end and 0.8 s after the hit. A dash ending does not cut short remaining hit protection. In 0.3 a quick dash after a hit could end that protection early. The 0.4 text says this no longer happens, and I found no contradiction with the spec.

### Regressions checked (description level only)

- Dash distance, duration and cooldown: unchanged.
- Enemies, rooms and attacks: "No other changes".
- Flicker and sound cues: **not checked**. The build text does not mention them.

### Undefined behavior and gaps

- The hit-stun dash press is unobserved in both builds (see blocker). The spec itself is defined by D-003.
- The one-frame difference at the 0.8 s and 0.25 s boundaries is stated, but not measured. A difference of more than one frame would be a failure, and it cannot be ruled out from prose.

### Plan once the case is observable

1. Press dash at several delays inside the 0.3 s hit-stun. Confirm that nothing fires then or when hit-stun ends (ignored, not buffered, per D-003). Also test an attack press. Do this at 30 and 60 FPS.
2. Run the matrix from handoff 10: dash delays of 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s. Keep a damage source present throughout. Record where damage lands: during the dash, between the dash end and 0.8 s, or after 0.8 s.
3. Repeat the earliest-dash case at least 20 times per frame rate.
4. Cover the no-hit dash, both directions, rooms 1–5 and both enemy types.
5. Record the boundary results at 0.8 s and 0.85 s at both frame rates.
6. Check the cooldown, queued attack and flicker/sound cues.

## Decisions already made

- D-001: Combat uses one attack button plus dash.
- D-003: Input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from `design/combat.md`, the acceptance criteria and the build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- Do not count the fix as verified until the open case is observed.

## Open questions

- For Studio and `gameplay-engineer`: state in the build, in observable terms, what happens when dash or attack is pressed during hit-stun. D-003 requires that it is ignored and not buffered. If the build does something else, that is a failure to route back.
- For Studio: confirm that `sim/build-0.4.md` (heading "0.3.1") is the intended latest build.
- For Studio: if observed run data (repeat counts, boundary timings) can be supplied, include it. If the dry run can only offer prose, say so, and QA will judge the other criteria on the prose with that limit recorded.

## Expected output

Studio routes the open case to `gameplay-engineer` for an observable statement, then re-routes to `qa` with the updated build file. QA returns a `pass` or `fail` verification report. If the case cannot be made observable, Studio should not count the fix as verified.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
