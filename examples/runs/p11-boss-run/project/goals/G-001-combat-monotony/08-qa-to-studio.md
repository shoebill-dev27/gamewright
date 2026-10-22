---
kind: handoff
goal: G-001
seq: 8
from: qa
to: studio
stage: Observe
outcome: done
---
# 08: qa → studio — 30 vs 60 FPS dodger discrepancy reproduced; build timing consistent, cause not isolated

## Task

Report on the 30 vs 60 FPS discrepancy in the balance-bot results and on dash invulnerability in the build (0.4). Studio decides the next routing.

## Context

Goal G-001 (combat monotony). The project constraint is "must play correctly at both 30 and 60 FPS". Studio handoff 06 reported that the dodger bot failed room 3 at 60 FPS and cleared it at 30 FPS. No build or bot change was made in this step; this is report only.

## Findings

### 1. Reproduction (bot results)

Script (`run_bots`, one script per rate, first line optional):

```text
bots camper,walker,dodger
rooms 1-5
fps 60        # second run: fps 30
```

Build at the time of the run: `repo/` 0.4 (the combat.md changes are SPEC for the next build and are not in this build).

| Bot / room | 60 FPS | 30 FPS |
|---|---|---|
| dodger room 3 | NOT cleared (19.7 s), 3 hearts lost (shot 3), attacks 3, dashes 13 | cleared 9.5 s, 0 hearts lost, attacks 6, dashes 4 |
| dodger room 4 | cleared 21.8 s, 2 lost (shot), dashes 9 | cleared 17.8 s, 2 lost (shot), dashes 6 |
| dodger room 5 | cleared 17.7 s, 1 lost, dashes 8 | cleared 17.8 s, 1 lost, dashes 8 |
| dodger rooms 1, 2 | 5.1 s and 7.1 s, 0 lost | 5.0 s and 7.0 s, 0 lost |
| dodger total | cleared 4/5, 6 hearts lost, 30 dashes | cleared 5/5, 3 hearts lost, 18 dashes |
| walker | 5/5 cleared, 1 heart lost in total (room 3, shot) | identical outcomes |
| camper | 2/5 cleared, 9 hearts lost | identical outcomes |

- **Reproduced**: yes, the 06 observation is exactly as reported.
- **Deterministic**: yes. Two identical 60 FPS runs gave byte-identical output. The game is headless and deterministic.
- **Where it stops**: only the dodger differs materially, in rooms 3 and 4. Rooms 1, 2, 5 and the walker and camper agree. Their clear times differ by at most 0.1 s, which is one frame of quantization.
- **Bots test**: `python3 -m unittest discover -s tests` passes (14 tests).

### 2. Does the simulation itself differ between 30 and 60 FPS? (traces)

Not in anything I could measure. Traces were taken in the practice room (`room empty`, `spawn`, `player`) at both rates:

- **Spitter timing**: the shot is fired at t=2.000 and t=4.000 at both rates.
- **Shot damage**: with no dash, the player is hit at t=4.250 at 60 FPS, losing 1 heart. Shot travel time is the same.
- **Dash distance**: 4.00 tiles at both rates (the test suite also checks this).
- **Dash duration**: the dash ends at t=0.250 at 60 FPS (frame 15) and t=0.267 at 30 FPS (frame 8). This is frame rounding of up to one frame.
- **Hit-stun and hurt-invulnerability**: a hit gives stun 0.300 s and invulnerability 0.800 s at both rates. The second grub hit comes 0.8 s after the first (t=0.250 → 1.050 at 60 FPS, 0.267 → 1.067 at 30 FPS).
- **Not directly traced**: grub walk speed and cooldown are computed from `dt` in the same way at both rates. I did not test them separately beyond the bot room runs.

So the simulation constants and event times agree within one frame. The measured discrepancy sits in the dodger bot's results.

### 3. Dash invulnerability vs `design/combat.md` ("invulnerable for the full dash duration")

The build matches at both rates in the cases I traced.

- **Dash into a grub** (`player 0 4`, grub at 0.5, 4, `0.0 dash left`): invulnerable from the dash press until the dash-timer-ended frame. The first hit lands at t=0.250 (60 FPS) and t=0.267 (30 FPS), in the same simulation step in which the dash ends. No hit occurs while the dash is active.
- **Dash through a shot**: in the practice room, a shot due to reach the player at about t=4.25 was crossed by a dash started at 4.1 s. The dash covered 4.1–4.35 s at 60 FPS and 4.133–4.367 s at 30 FPS. No hurt event occurred at either rate. The control run without the dash was hit at t=4.250.
- **Invulnerability handoff**: the trace shows invulnerability dropping on "dash timer ended" and being re-set by "hurt" in the same step. This is consistent with the spec and with the existing test.
- **Not tested**: a dash started while hurt-invulnerable (the existing test `test_a_dash_right_after_a_hit_keeps_both_protections` covers it at both rates and passes), and dash against a lunging grub (not in this build).

### 4. Defect assessment

- **Build defect confirmed?** No. I found no build behaviour that differs between 30 and 60 FPS beyond ±1 frame rounding.
- **Bot issue?** Likely, but not isolated. This is a hypothesis, not a finding: the dodger acts every frame, with no reaction delay, and dashes whenever a shot is detected and the dash is ready. Dashes are 4 tiles long. A one-frame difference in when a shot is first detected, or in where the dash ends, may be enough to shift later decisions in a chaotic way (13 dashes at 60 FPS vs 4 at 30 FPS in room 3). Note that `play.py` limits rules to one action per 0.15 s but `bots.py` does not.
- **Ruled out**: non-determinism; differing spit timing, dash distance, hit-stun and hurt-invulnerability timing; dash invulnerability missing at either rate in the traced cases.
- **Not ruled out**: an unnoticed 30/60 difference in a case I did not trace, for example shot reach and position checks while the player is dashing past a shot at different frame offsets. I did not examine this. I could not produce a per-frame bot decision log because `bots.py` only prints summaries and I may not change it.
- **Cannot yet say** whether the dodger's room 3 result "should" be the 30 FPS or the 60 FPS result. Neither rate is defined as correct by the spec.

### 5. Severity and frequency

- **Severity**: medium for the project's evaluation. The discrepancy affects bot-based balance verification, not the player, as far as measured. If the cause turns out to be the build, it would be a constraint violation.
- **Frequency**: always reproduced at the given scripts (deterministic).

### 6. Effect on the 07 spec's acceptance criteria

`design/combat.md` criteria 13–16 depend on the dodger behaving the same at both rates, and the existing bots do not react to the new cues. They stay conditional. Criteria 1–12 cannot be run against build 0.4 at all (grub wind-up, aim cue, new rooms and variants are not in the build).

## Decisions already made

None.

## Constraints

- No change to the build or bots was made.
- Must play correctly at both 30 and 60 FPS (project.md#constraints).

## Open questions

- Is the room 3 / room 4 dodger split purely a bot-sensitivity effect? To settle it, either update the dodger with a frame-rate-independent reaction (an accumulated-time reaction delay like `play.py`'s 0.15 s) and re-run, or log the dodger's per-frame decisions, e.g. via a `gameplay-engineer` change to `bots.py`.
- Suggested check for that next run: a reaction-rule script in `play.py` (for example `when see * coming within 2 then dash aside` plus the walker-like rules) in room 3 at 30 and 60 FPS. If it gives the same outcome at both rates, the build is not the cause.
- Which of the two results should count as the dodger baseline for criterion 13? Studio / `game-designer` to say once the bot is fixed.

## Expected output

This report. Proposed next step by Studio:

- Route to `gameplay-engineer` to make the dodger bot frame-rate independent (accumulated-time reaction delay) and to add reaction to the new cues. Do not change the build for this.
- Afterwards, QA re-runs the bots at 30 and 60 FPS (`bots camper,walker,dodger`, `rooms 1-5`, both rates), and verifies criteria 13–16.

If a defect is later confirmed in the build, acceptance criteria for the fix:
1. The same bot script gives equal pass/fail per room at 30 and 60 FPS, with hearts lost within ±1 and clear time within ±0.5 s.
2. Traces of dash into a grub and through a shot show no hurt event during the dash at either rate.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, repo/bots.py, repo/game.py, repo/play.py
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/06-studio-to-qa.md
