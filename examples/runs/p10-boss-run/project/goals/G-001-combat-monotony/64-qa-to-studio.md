---
kind: handoff
goal: G-001
seq: 64
from: qa
to: studio
stage: Observe
outcome: done
---
# 64: qa → studio — 30 FPS coverage closed: player view (rooms 1–5) and late-swipe boundary match the design and 60 FPS; no defect; one spec conflict on shots in flight (room 3) for Design

## Task

Close the two gaps left by handoff 56: the player view at 30 FPS for rooms 1–5, and the late-swipe boundary at 30 FPS for a grub and a runner. Report any difference from 60 FPS or from `design/combat.md`.

## Context

Goal G-001. The build was not changed. Evidence comes from this step's runs only:
- `python3 -m unittest discover -s tests`: 59 tests, OK.
- Player view at 30 and 60 FPS for rooms 1–5. They are reaction scripts, as in handoff 55. Rooms 3–5 ran 12–15 s.
- Practice-room traces at 30 and 60 FPS for the grub and runner, in reach and out of reach.
- Grub swipes at 0.40, 0.50, 0.52 and 0.60 s, and a room 1 reaction trace at both rates.

## Findings

### 1. Player view at 30 FPS, rooms 1–5: matches the design, the manual and 60 FPS in everything the rules fix

**Warnings and cue lines**
- Every grub, runner and brute wind-up printed `a grub rears back` and a picture with `~`. A `cue:` line named the enemy (`g`, `r`, `G`) and gave the lane direction, 2.4 tiles, and the seconds left.
  - Standard grub: starts at "0.50 s", e.g. room 1, 2.033 s.
  - Runner: "0.35 s", e.g. room 2, 3.000 s.
  - Brute: "0.70 s", e.g. room 2, 25.967 s, and room 5, 5.000 s.
- The countdown falls consistently between prints, e.g. 0.50 → 0.03 s in room 1. The 60 FPS runs show the same values within one frame.
- The line disappears when the lunge starts. The manual and `combat.md` accept this.
- Spitters: `a spitter takes aim` → `a spitter spits` is 0.6 s apart at both rates. Brightness rises 0% → 33% → 50% → 83% in the `cue:` lines. The text view starts at 0%, as ruled in step 22.

**Spitter timing**
- Room 3, first shots: 1.8, 2.6 and 3.4 s at both rates.
- Rooms 4 and 5, first shots: 1.8 and 3.0 s at both rates.
- Cue gap in rooms 4–5 at 30 FPS:
  - Room 4: shots at 1.8, 3.0, 4.2, … with the next cue starting 0.6 s after each. Cues are 2.4 → 3.0, 3.6 → 4.2, 6.8 → 7.4, 8.0 → 8.6, and so on.
  - Room 5: 7.000 → 7.600, then 8.400 → 9.000. The gap is 0.8 s, which is at least 0.6 s.
  - No cue windows overlap.
- Cap delay in room 5 at 60 FPS: the cue due at 6.0 s was delayed to 7.0 s. This is allowed.

**Hit messages**
- `YOU ARE HIT by a grub — hearts n/3` and `… by a shot …` appear on the frame of contact.
- Shot hits: room 3 at 5.633 (30 FPS) against 5.667 (60 FPS), and room 5 at 4.333 against 4.350. That is within one frame.

**Brute**
- Room 5, a swipe during the wind-up:
  - 30 FPS: 7.867, a swipe 0.07 s before the lunge. It printed `the brute shrugs off the swipe`, the cue stayed, and the hit followed at 8.000.
  - 60 FPS: 8.517, same behaviour, with the hit at 8.783.
- Room 2, 30 FPS: swipes during the lunge (26.733) and recovery (27.233, 27.733) printed only `you swipe: brute hit`, with no shrug message. The fourth hit, at 28.100, printed `brute defeated` with no shrug message, even though the brute was already winding up (cue at 28.067). That matches criterion 19c: a killing swipe in wind-up shows no message and there is no lunge.

**One at a time and cancel**
- Room 5, 30 FPS: a swipe at 7.033 cancelled the winding-up grub. Its cue vanished and the next wind-up was the brute's, at 7.233.
- Room 1, 30 FPS: a second grub began its wind-up (2.800) only while the first was in recovery.

**Blocked contact (D-005) seen unprompted at 30 FPS**
- Room 1 reaction trace: the player was hit at 2.767, so the window ran to 3.567.
- The grub's lunge touched the player at about 3.467 (grub at 7.11, player at 7.47) while protected.
- At 3.567 the window ended with the grub still lunging, 0.43 tile from the player. Hearts stayed at 2, and the grub went into recovery at 3.733.
- This matches criterion 21b: the lunge's hit is spent.
- At 60 FPS the same room gave a hit at 3.567 instead. That timeline differs: the player was at 7.87, and first contact came after the window had ended, which is a legitimate hit.

**Differences between 30 and 60 FPS in the reaction scripts**
- Final outcomes differ:
  - Room 1: cleared at 1 heart (30 FPS) against down at 5.83 s (60 FPS).
  - Room 2: cleared at 28.1 s (30 FPS) against 11.7 s (60 FPS), both with 1 heart.
  - Room 5: 1 heart at 15 s with 2 enemies left (30 FPS) against 3 left (60 FPS).
  - Rooms 3 and 4: the same hearts at 12 s and 15 s.
- The reaction rules act on a 0.15 s grid, so positions diverge early. Examples are the room 2 grub that was avoided for many seconds at 30 FPS, and the different paths in room 1.
- I did not isolate a case of the same decision from the same state at the same time giving a different result. By criterion 16d/16e this is bot-timing sensitivity, not a finding. I make no claim beyond that.

**Verdict for item 1: matches. No difference in warnings, cue lines or messages between 30 and 60 FPS beyond one-frame timing.**

### 2. Late-swipe boundary at 30 FPS: matches the design, and differs from 60 FPS by less than one 30-FPS frame

Practice room, grub at 9.3 or 10, player at 8,4. A scripted input fires on the first frame after its timestamp at both rates (0.50 → frame 16 at 30 FPS and frame 31 at 60 FPS). Within a frame, the swipe is resolved before the grub's wind-up timer expires.

**Standard grub**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe mid-wind-up (0.40) | swipe at 0.433: stagger 0.367, hp 2→1, no lunge, new wind-up at 0.833 | swipe at 0.417: stagger 0.383, no lunge, new wind-up at 0.817 |
| In reach, swipe on the frame the lunge starts (0.50) | swipe at 0.533, frame 16: **cancelled** (stagger 0.367) | swipe at 0.517, frame 31: **cancelled** (stagger 0.383) |
| In reach, swipe one frame after the lunge starts (0.52) | lunge 0.533, swipe 0.567: hp 2→1, lunge continues, hit at 0.633 (hearts 3→2) | lunge 0.517, swipe 0.550: same, hit at 0.617 |
| In reach, swipe 0.60 (late) | swipe 0.633 with the hit in the same row; not cancelled | swipe 0.617 with the hit in the same row; not cancelled |
| Out of reach (grub starts 2 tiles away), swipe 0.30 | `hits: []` at 0.333; wind-up unchanged (0.200 left); lunge at 0.533; hit at 0.733 | `hits: []` at 0.317; lunge at 0.517; hit at 0.700 |

- At both rates the last swipe that cancels is the one landing on the frame the lunge begins. A swipe one frame later does not cancel.
- Lunge start is 0.533 s at 30 FPS and 0.517 s at 60 FPS. The difference is 0.017 s, half a 30-FPS frame. The cancel limit therefore differs by under one frame at 30 FPS.
- The 60 FPS probes bracket the boundary between frames 31 and 33. I did not probe frame 32.
- Lunge hit times differ by one to two frames (0.733 against 0.700, 0.633 against 0.617), which is frame sampling.

**Runner**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe 0.20, mid-wind-up | `runner defeated` at 0.233; no lunge; cleared | `runner defeated` at 0.217; same |
| In reach, swipe 0.43, after the lunge began | lunge 0.400, swipe 0.467: runner defeated before contact; hearts 3 | lunge 0.367, swipe 0.450: same; hearts 3 |
| Out of reach (2 tiles), swipe 0.20 | `hits: []`; wind-up continues; lunge 0.400; hit 0.600 (hearts 3→2) | `hits: []`; lunge 0.367; hit 0.550 |

- The runner's out-of-reach swipe does not cancel at either rate.
- The runner has 1 hp, so an in-reach swipe always kills it. The "a late swipe does not cancel the lunge" case is not separable from a kill for a runner. It showed as a kill at both rates, with the lunge ending before contact. The spec cannot tell "cancel" from "kill" for a runner, and I report it as observed behaviour only.
- After the first hit, the second runner lunge fell at 1.600 s (30 FPS) against 1.517 s (60 FPS), a 0.083 s gap. It comes from the earlier contact-frame difference of 0.05 s plus frame quantization. Both rates took two hits.

**Verdict for item 2: matches. At 30 FPS the cancel boundary sits at the frame the lunge starts, as at 60 FPS, and differs by less than one 30-FPS frame.**

### 3. Defects: none

I found nothing that is wrong against `design/combat.md` or `repo/manual.md`. One conflict inside the spec, found while reading the room 3 views, is below. It is not a build defect.

### Spec gap for `game-designer` (not a defect, low to medium priority): room 3 shots in flight, and simultaneous cue starts in a real room

**What the room 3 reaction runs show (same at 30 and 60 FPS)**
- All three spitters started a cue at the same moment twice: 5.800 (at both rates) and 10.000 (30 FPS) or 9.800 (60 FPS). In both cases all three then fired together 0.6 s later.
- Their checks run on the same 0.2 s grid after cap delays. The first start at 5.8 s followed the hit by a shot at 5.633 / 5.667 s, which freed a cap slot. This is my reading of the pattern and is not confirmed in code.
- This is the "real-room trace in room 3 with a surviving player past 7 s" asked for in `combat.md` open questions and D-005 (revisit).
- In both runs the player (a reaction script with "move aside") took no hit from the simultaneous volleys. Hearts stayed at 2 from 5.8 s to 12 s. The lines did cross at the player's row (30 FPS, 10.0 s). So this case did not show unanswerable shots.
- At least 4 `*` are visible in flight at 7.0, 7.5 and 8.0 s at both rates. Up to 5 would be expected: two earlier shots plus the three fired at 6.4 s. Criterion 11 says "in rooms 1–5 never more than 3 shots in flight". The cap section says real rooms stay at 3 or fewer, citing a QA observation, and also says the count at a check can reach 2 + the number of living spitters. For three spitters that is 5.
- I counted `*` from the pictures only. I did not run a trace for the exact count, and shots in the same cell as a spitter can be hidden. I cannot say whether the number is exactly 4 or 5.

**Question for Design:** is the simultaneous start in room 3 still accepted (D-005), and is "never more than 3 in flight in rooms 1–5" still the rule in room 3? The two statements conflict when a cap delay releases all three spitters at once.

**Reproduction:**
```text
room 3
fps 30
end 12
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when see s within 1.4 then attack
```
Run it at `fps 30` and `fps 60` and look at the cue starts at 5.8 s and the stars at 7.0–8.0 s.

**Acceptance criterion if Design wants a change:** in a trace of room 3 with a moving player over 12 s, the shot count never exceeds the number the spec states, at both frame rates.

## Decisions already made

- D-002/D-003: contact-edge graze. No contact in these runs was in the band. The lunge contacts were at lateral miss 0 against 0.6.
- D-004: the brute is not cancelled by a swipe. Confirmed at both rates (see item 1).
- D-005: a lunge's hit is spent when it touches a protected player. Seen at 30 FPS (room 1) and consistent with the room 5 observations in handoff 56. The simultaneous-start acceptance is raised again above because the revisit trigger has now been traced.

## Constraints

- The build and documents were not changed.
- Not run:
  - A frame-32 probe at 60 FPS.
  - A brute late-swipe boundary pair, beyond the room 2 and 5 views.
  - Dash cases at 30 FPS.
  - A trace of room 3 for the exact in-flight count.
  - A human playtest.
  - Isolating the 30/60 FPS reaction-script divergences.
- Experience judgments (monotony, fun) are not assessed here.

## Open questions

For `game-designer`:
1. The room 3 shot-count conflict and the simultaneous-start acceptance (above).
2. The manual wording from handoff 56 is still open. It should say a swipe cancels a lunge only during the warning, and not when the grub is out of reach. This step again showed an out-of-reach swipe that did nothing (2 tiles, `hits: []`, at both rates) and the cancel limit at the lunge start.
3. For a 1-hp runner, "cancel" and "kill" cannot be told apart by a swipe in reach. If the design means a separate runner cancel rule, it does not show up in play.

## Expected output

Studio: record the two 30 FPS gaps as closed and matching. Route the room 3 in-flight-count and simultaneous-start question to `game-designer`. No change is requested from `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, the build in repo/
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/62-studio-to-qa.md
