---
kind: handoff
goal: G-001
seq: 15
from: qa
to: studio
stage: Observe
outcome: done
---
# 15: qa → studio — Defect report: identical "a spitter spits" lines at one timestamp (rooms 4–5)

## Task

Studio: route this report. The doubled line is reproduced. It is two spitters each printing one line, not one event printed twice. The defect is presentation only: the two lines are identical and do not say which spitter fired.

## Context

Handoff 12 asked whether the repeated spitter attack line is one event printed twice (a defect) or two spitters each printing their own line (one line per spitter). It also asked in which rooms it occurs and whether it changes with spitter count. Build under test: `repo/` at sha e54837757611 (the player view header reads "Lantern Depths 0.4"). All evidence comes from the run commands in `project.md`, driven by input scripts.

## Findings

### Verdict

- **Reproduced: yes.** Every volley in rooms 4 and 5 prints two identical lines at the same timestamp.
- **Cause class: two events, not one event printed twice.**
  - With one spitter, the trace shows one `spit` event per volley.
  - With two spitters, the trace shows `spit; spit` per volley.
  - So the count of lines follows the count of spitters, i.e. one line per spitter. That matches the "one line per spitter" expectation stated in handoff 12.
- **What is wrong:** the text is the same for both spitters ("a spitter spits"). It carries no name or position, so the player cannot tell the lines apart and reads them as a duplicate. This is a presentation defect. It is not a logic or double-fire defect.

### Reproduction

Script A (player view, room 4):
```
room 4
fps 60
end 5
```
Command: `python3 play.py --view player {script}`

Observed:
```
  2.000  a spitter spits
  2.000  a spitter spits
  4.000  a spitter spits
  4.000  a spitter spits
```

Script B (trace, one spitter):
```
room empty
fps 60
spawn spitter 15 0
player 8 4
end 6
```
Observed: a single `spit` event at t=2.000, 4.000 and 6.000.

Script C (trace, two spitters):
```
room empty
fps 60
spawn spitter 15 0
spawn spitter 15 8
player 8 4
end 6
```
Observed: `spit; spit` at t=2.000, 4.000 and 6.000. The projectile count follows: the player view shows two `*`, one per spitter, so the pair is two shots and not a duplicate print.

### Conditions varied

| Condition | Result | View used |
|---|---|---|
| Room 4, 60 FPS | Pair of identical lines at 2.0, 4.0, 6.0, 8.0 s | player and trace |
| Room 4, 30 FPS | `spit; spit` at 2.0, 4.0, 6.0, 8.0 s, same as 60 FPS | trace only |
| Room 5, 60 FPS | `spit; spit` at 2.0, 4.0, 6.0, 8.0 s | trace only |
| 1 spitter (practice room) | One `spit` per volley | trace only |
| 2 spitters (practice room) | `spit; spit` per volley | trace only |

- **Frame rate:** the script format has an `fps 30|60` line, so both frame rates can be set. The behavior and the timestamps are the same at both.
- **Rooms:** it occurs in both room 4 and room 5, because both have the same two corner spitters at (15,0) and (15,8).
- **Spitter count:** the number of identical lines equals the number of spitters. Room 3 (3 spitters) was not run; I expect three identical lines there, and that is a hypothesis, not an observation.

### Not run (round budget)

- The player-view text for room 5 and for the one-spitter case. The trace `spit` events were used as the evidence there.
- The player view at 30 FPS.
- Room 3.

### Expected, and its source

- `design/combat.md` AC-8 (build 0.5 target): "The spit line names its spitter; there are no identical duplicate lines at one timestamp."
- AC-8 describes the target build, not the current one. No document defines the current build's line text as a defect. The current build behaves as "one line per spitter", which is what handoff 12 says the design expects. The defect is therefore measured against AC-8, which the planned spitter rework must satisfy. It is not a regression against an earlier spec.
- The cause of the missing name is not known. A plausible hypothesis (unverified) is that the line text is a fixed string that does not take the spitter's identity.

### Severity and frequency

- **Severity: cosmetic / low.** The mechanics are unaffected. The cost is readability: the player cannot tell which spitter fired, and the repeated line looks like a bug.
- **Frequency:** every volley in rooms 4 and 5 (about every 2.0 s on the current build), 100% of volleys.

### Evidence

The trace rows for the room 4 runs at 30 and 60 FPS, the room 5 run at 60 FPS, and the one-spitter and two-spitter runs are quoted above and in the run results of this step.

## Decisions already made

None bear on this defect.

## Constraints

- Report only what is observable on the current build; no fix is proposed.
- The rest of the Option A spec was not verified or commented on.

## Open questions

None for the Owner. Process note for the Studio: the observed behavior matches "one line per spitter", so this is not a duplicate-event bug. Treat it as presentation covered by AC-8, to be verified after the rework.

## Acceptance criteria for the fix

1. In rooms 4 and 5, at both `fps 30` and `fps 60`, each spit line names its spitter (for example by position, as in "spitter (top right) spits").
2. No two lines printed at the same timestamp have identical text, for any spitter count (check 1, 2 and 3 spitters; rooms 3, 4 and 5).
3. The number of spit lines at a timestamp equals the number of spitters that fired, and the number of `spit` trace events is unchanged.
4. Each spit line can be matched to its projectile (that spitter's `*`).
5. Spit timing and projectile behavior are unchanged by this fix, apart from whatever the rework intentionally changes.

## Expected output

Studio routes this defect report to the owner of the spitter rework, as a presentation requirement alongside AC-8.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
