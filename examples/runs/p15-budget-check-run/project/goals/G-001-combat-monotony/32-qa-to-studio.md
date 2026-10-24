---
kind: handoff
goal: G-001
seq: 32
from: qa
to: studio
stage: Triage
outcome: done
---
# 32: qa → studio — Room 2 "grub hit right after a swipe": not a build defect (swipe landed during the lunge); manual wording is misleading

## Task

Report whether the playtester's room 2 observation (handoff 27, item 5) is a defect, a rules-conforming case, or not reproducible. Verdict: **not a build defect. It reproduces, and it conforms to design/combat.md.** One low-severity documentation wording issue is noted for routing.

## Context

Goal G-001. The playtester reported:

- a grub rearing back at about 5.37 s;
- "grub hit" from their swipe at about 5.9 s;
- a grub hit on the player at about 6.017 s.

They asked whether the swipe failed to cancel the lunge or a second grub hit them. The exact script was not preserved. I reconstructed a comparable reaction-rule script (sidestep on "rears back", swipe things within 1.4, approach) and ran `run_trace` at 60 and 30 FPS in room 2. `run_tests` passed (34 tests, OK).

## Findings

### Timeline check against the playtester's numbers

Wind-up for a standard grub is 0.5 s, so a wind-up starting at 5.37 s turns into a lunge at about 5.87 s. The swipe at 5.9 s therefore landed about 0.03 s after the lunge began, not during the wind-up. The grub is then in flight, and the hit at 6.017 s is the lunge reaching the player, about 0.1 s later. The playtester's timeline fits one grub whose swipe came too late to cancel. I derived this from the numbers and could not check it against the original run.

### Trace evidence, 30 FPS (same pattern reproduced)

| Time (s) | Event |
|---|---|
| 2.633 | grub `windup:0.500` |
| 3.133 | grub `lunge` begins |
| 3.300 | `attack {'hits': [('grub','hit')]}`: grub hp 2→1, phase still `lunge` (grub at about (11.95,3.25), player (11.60,4.13), distance about 0.95, within the 1.5 reach) |
| 3.367 | `hurt {'source':'grub','hearts':2}`, 0.067 s after the swipe; the grub goes to `recovery:0.800` |

The sequence is the same as the playtester's: "grub hit", then hurt about 0.07–0.1 s later. It is the same grub, there is no second grub, and the lunge was already in flight when the swipe landed.

The same pattern appears for a brute at 30 FPS: swipe hit during `lunge` at 4.567, hurt at 4.633, source labelled `grub` (the brute is a brute grub). A runner lunge also hit at 5.933 on the same frame the swipe defeated a brute.

### Trace evidence, 60 FPS

- 4.033: grub `windup:0.500`. The player was at (12.93,5.27) and the grub at (12.79,3.60), so the distance was about 1.68, **outside the 1.5 swipe reach**. The swipes at 4.033–4.483 hit or killed the brute. The attacks at 4.183 and 4.333 were ignored as `recovering`.
- 4.533: lunge. 4.650: the player is hit, and the grub stops early at contact and goes to `recovery`.
- Here the swipe never reached the winding-up grub, so this is not a failed cancel.
- 5.033: a swipe hits the grub in recovery (hp 2→1), phase unchanged.
- 5.467: the grub winds up again. 5.500: a swipe kills it during wind-up with no stagger and no lunge, which matches the "kill in wind-up" rule.

### Not the D-002 graze

The lunge contacts were not edge cases. The grub stopped about 0.5 tile (60 FPS: (12.83,4.53) vs player (12.87,5.07), distance about 0.54) from a stationary player in the lane's center. That is far from the 0.57–0.60 band, and the hit came from the player standing in the lane, not from a near-reach path.

### Expected vs actual

- Expected (design/combat.md, Grub rules): "A swipe that damages a grub in wind-up cancels the wind-up." Also: a grub hit but not killed during Lunge "continues its phase unchanged", and a lunge that reaches the player deals 1 damage unless the player is invulnerable.
- Actual: the swipe landed in the lunge, the lunge continued, and the hit followed. This conforms.
- Documentation conflict (low): `repo/manual.md` says "step 1 tile to the side, dash, or swipe it (within 1.5 tiles) to cancel the lunge." It does not say the swipe only works during the warning, and "cancel the lunge" can read as covering a lunge already moving. combat.md is clear and says a lunge in flight is not cancelled. The manual's own warning duration (0.5 s) hints at the limit but does not state it. This is a manual wording gap, not a build defect. Fixing it is a manual change, and I do not decide intended player-facing wording.

### Classification, severity, reproducibility

- Defect: none found. Rules-conforming, with the documents agreeing on the build's behavior.
- Reproducibility: the pattern reproduced at 30 FPS (grub and brute) and the timing arithmetic fits the playtester's report. At 60 FPS my script did not produce the same sequence, because the swipe never reached the winding-up grub. I did not run a controlled 60 FPS case of a swipe landing just after lunge start.
- Severity of the manual wording issue: low (it can mislead a player about when the swipe cancels). Frequency: any swipe that lands after the wind-up ends.

### Not covered

- The exact original script and its trace are unavailable, so the match is by arithmetic and a comparable reproduction.
- I did not observe a non-lethal swipe during wind-up (the "cancel plus 0.4 s stagger" case) in these traces. The tests passed, but I did not inspect which tests cover it.
- I did not check at code level how the 1.5 reach is measured. The distances above come from trace positions.
- No unit or script was changed. The build was not modified.

## Decisions already made

- D-002: per-frame contact sampling kept, graze accepted. This case is not the graze (see above).

## Constraints

Report only, verified from design/combat.md, repo/manual.md, D-002 and the build (trace, tests). The build is unchanged.

## Open questions

- For `game-designer`: should the manual say explicitly that a swipe only cancels a lunge during the wind-up, and that a lunge already moving is not cancelled (the grub stays hittable and the lunge still hurts unless the player dashes or sidesteps)? This is wording, not a rule change. The combat.md rule is unambiguous, so no ruling on intent is needed. Whether to reword the manual is the designer's call.
- Related and optional, for the same designer: nothing else is raised by this case.

## Expected output

Studio decides routing: close handoff 27 item 5 as not-a-defect, and send the manual wording question above to `game-designer` (low priority). No fix is requested from `gameplay-engineer`.

If the studio wants more evidence, a controlled practice-room script (`room empty`, `spawn grub`, `player`, swipe at 0.45 s vs 0.55 s after the cue) at fps 30 and 60 would show the two sides of the 0.5 s boundary. I did not run it, since the verdict does not depend on it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/29-studio-to-qa.md
