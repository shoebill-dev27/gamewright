---
kind: handoff
goal: G-001
seq: 36
from: qa
to: studio
stage: Observe
outcome: done
---
# 36: qa → studio — Spitters in rooms 3–5: build 0.5 conforms to the 0.5 spec at 30 and 60 FPS; the "sync" report is explained but not reproduced in a real room; one spec gap on shots that touch an invulnerable player

## Task

Check whether the spitters in rooms 3 and 4 (and 5) fire at the positions and times `design/combat.md` specifies, how many shots are in flight, and whether the playtest observations are defects.

## Context

G-001. Evidence: `run_trace` of rooms 3, 4 and 5 with a player who does nothing (30 and 60 FPS), plus two scripted practice-room traces. Those traces used the room-4 spitters at (15,0) and (15,8), the player at (8,4), a sidestep down 1 tile during the first cue, and in one script a return to y=4 (30 and 60 FPS each).

Per the spec header, build 0.5 behaves **without** the step 35 parts. So the expected 0.5 values are offset 0.8 s in every room, and no cue-gap rule. The trace does not print projectiles. "Shots in flight" below is derived from fire times, the 3.0 tiles/s speed and the hit times, and I label it as derived.

## Findings

### 1. Positions: match the spec's room table

- Room 3: spitters at (2,1), (14,7), (2,7). Match.
- Room 4: runner (1,4), standard (0,1), spitters (15,0) and (15,8). Match.
- Room 5: standard (1,1), standard (0,6), brute (4,8), spitters (15,0) and (15,8). Match.
- The "opposite corners" vs "same side" question has a simple answer. In rooms 4 and 5 both spitters are on the **east wall (x=15)**, one at the north end and one at the south end. A playtester would call that "opposite corners". The Studio's reading of "same side" is also correct. They do not contradict each other. The spec has no layout the build departs from.

### 2. Times: match the 0.5 spec at both rates

- **First shots.**
  - Room 3: 1.8, 2.6 and 3.4 s, at both rates.
  - Rooms 4 and 5: 1.8 and 2.6 s, at both rates.
  - The cue (`cue=True`) starts at `fire_in=0.600` and the shot is at 0.6 s later, within one frame, at both rates.
  - The rooms 4–5 times of 1.8 and 2.6 s are the 0.5 default (offset 0.8). The step 35 value (1.8 and 3.0 s) is not in the build yet.
- **Interval.** Room 4 spitter at (15,0): 1.8 then 4.2 s, an interval of 2.4 s. Other shots are later than the nominal 2.4 s only by the cap delay:
  - Room 4 spitter at (15,8): nominal 5.0 s, observed 5.2 s. Derived: the cue was due at 4.4 s with 3 shots in flight, and was released at 4.6 s once the 1.8 s shot was spent.
  - Room 3 spitter at (2,1): nominal 4.2 s, observed 4.6 s. Derived: the cue was blocked at 3.6 s with 3 in flight and released at 4.0 s.
  - This is the "delay carries forward" rule (spec "Cap delay").
- **Rate differences.** All fire and cue times match between 30 and 60 FPS to within one frame. Hit times differ by about one frame, as expected.

### 3. Cue windows and gaps (rooms 4–5, still player, both rates)

- Room 4 cues: spitter (15,0) at 1.2–1.8, spitter (15,8) at 2.0–2.6, spitter (15,0) at 3.6–4.2, spitter (15,8) at 4.6–5.2.
- Room 5 has the same pattern up to the observed times.
- No cue windows overlap.
- The gap from a shot to the next cue **start** by the other spitter is **0.2 s** at 1.8 → 2.0, and **0.4 s** at 4.2 → 4.6.
- That is the 0.5 behaviour ("old 0.2 s between consecutive cues"). It is below the step 35 rule of 0.6 s, as expected for 0.5.
- It explains why a player who sidesteps the first line can have the second spitter lock onto them 0.2 s later, which matches "hit while lined up for another warning".

### 4. Simultaneous fire: reproducible in the practice room, not observed in a real room

- In the practice-room replica of room 4 (script `d4-*-back`, both rates), **both spitters start a cue at 6.8 s** (`aim; aim`, both `fire_in=0.600`) and would both fire at 7.4 s. Both rates agree.
- Derived cause:
  - The (15,0) spitter's cue was due at 6.0 s. It was blocked by the cap, because the missed 2.6 s shot was still alive (shots live up to 5 s), plus the 4.2 s and 5.0 s shots.
  - It was released at 6.8 s, after the 4.2 s shot hit at 6.733.
  - The (15,8) spitter's cue was due at 6.8 s. Both therefore start together.
- This matches the playtester's "fired in sync", but only through the cap delay on a player who survives.
- The 0.5 spec text has nothing that stops two cues starting together (cap counts shots only; the spec allows up to 2 + the number of living spitters in flight). The 0.5 build conforms to its text. The step 35 gap rule would prevent this case.
- **Not shown in a real room:** my still player in rooms 4 and 5 dies at about 5.3 s and 6.2 s, before any cap delay. I have no real-room trace past 7 s.

### 5. Shots in flight (derived)

- Room 3: 3 in flight from 3.4 to 3.9 s, then 2, then 3 again with the 4.6 and 5.0 s shots. Never above 3 (spec limit: cap check of fewer than 3 at cue start).
- Room 4 (and 5): 3 in flight at 4.2 s (shots from 1.8, 2.6 and 4.2 s). The cap blocks the next cue until a shot is spent.
- Practice replica: 3 in flight from about 5.0 to 6.7 s (derived). It stays within 2 + the number of living spitters.
- No count exceeded the spec in any trace. I did not see a printed projectile count.

### 6. Hits: which cause

Cause names: **in flight** = a shot already fired that reaches the player; **new lock** = a cue that starts after the player has moved and aims at their current position; **misread** = the player re-entering a line.

- **Player stays still (rooms 3, 4, 5).**
  - Every shot hit is a shot aimed at the standing player at its cue start. It is already in flight by the time it arrives, about 2.1–2.55 s after firing.
  - Room 3: hits at 3.9, 4.7 and 5.5 s (down at 5.5 s, with no input at all).
  - Room 4: runner lunge at about 3.7 s, then shots at about 4.5 s and 5.3 s.
  - Room 5: shots at 4.33 s and 5.13–5.15 s, then the brute lunge at about 6.15 s (down).
  - This is "standing still is punished", as specified.
- **Player dodges one line (practice replica).**
  - Sidestep down during the first cue (1.3–1.55 s): the first shot passes at a lateral miss of about 0.87 tile (derived). No hit at either rate.
  - If the player **stays** at the new position, the next cue (2.0 s) locks there, and the 2.6 s shot hits at 4.97 s (30 FPS) and 5.0 s (60 FPS). Cause: **new lock** on the standing player.
  - Later hit at 6.93 s: a **new lock** again (cue at 3.6 s locked on y=5).
  - If the player steps back up (2.1 s), the 2.6 s shot misses. Then they stand at (8,4) and are hit at 4.33 s (30 FPS) and 4.35 s (60 FPS). That is the original **in flight** shot from 1.8 s, still flying along its line, and the player stepped back into it. Cause: **in flight, misread** by the player. It is not a build error. The shot's line is the original line.
  - The hit at about 6.75 s is a **new lock** on the standing player.
  - I saw no hit on a player who had left a line and stayed out of it.

### 7. Spec gap (not a defect): a shot that touches an invulnerable player is not consumed

- Room 4, still player. The first shot from (15,0) (fired at 1.8 s) should reach the player at about 4.35 s (derived: path 8.06 tiles minus the 0.4 reach, at 3.0 tiles/s). The player is invulnerable from the runner hit at 3.7 s until 4.53 s (30 FPS) or 4.48 s (60 FPS).
- The shot's damage lands **exactly when the hurt invulnerability ends** (4.533 at 30 FPS, 4.483 at 60 FPS). The same happens with the second shot: derived arrival 5.15 s, hit at 5.333 (30 FPS) and 5.283 (60 FPS), again the moment the hurt window ends.
- Hypothesis (not confirmed in code): a shot whose contact is blocked by invulnerability is not removed and is still within reach when the window ends.
- The spec says a shot "disappears … on contact with the player" and "invulnerability stops the damage". It does not say whether a blocked contact consumes the shot, and "two shots arriving together" only says at most 1 damage per window. **The expected behavior is not defined, so this is for `game-designer`, not a defect.**
- Player-visible effect: a hit can land 0.15–0.2 s after the shot visibly reached the player, and close hits can chain at the end of each 0.8 s window. This probably contributes to the "hit while lined up" and quick deaths in rooms 4–5.
- Severity if the designer rules it unintended: medium (hurts the experience). Frequency: any shot arriving during i-frames and still within 0.4 tile when they end. Not seen with the dash, because I did not test one.
- Observation (not a defect): in room 3 the three hits are 0.8 s apart, which equals the invulnerability window, so a still player loses all 3 hearts in 1.6 s.

### Verdict

- **Build 0.5 conforms to the 0.5 spec** for spitter positions, first-shot times, cue timing (0.6 s ±1 frame), interval and cap delay, and in-flight count, at 30 and 60 FPS.
- **Differs from the step 35 spec (0.6)** in rooms 4–5, as expected: offset 0.8 instead of 1.2, no 0.6 s gap rule. Criterion 18 does not apply to 0.5.
- No defect found. Two items go to `game-designer`: the invulnerable-contact gap (finding 7), and whether simultaneous cue starts after a cap delay in room 3 should be prevented (the step 35 gap rule only covers rooms 4–5).

## Decisions already made

- D-002: graze accepted. No reported hit was in a graze band. The shot lateral miss is not near 0.39–0.40 in any case above.

## Constraints

Report only. The build, tests and scripts in `repo/` are unchanged.

## Not covered

- The playtester's deaths at 15.75 s (room 4) and 11.1 s (room 5), the room 3 double fire at about 5.8 s, and their scripts: not reproduced. I had no script, and my still player dies at about 5.3–6.2 s. In my room 3 still trace nothing fires at 5.8 s before the death at 5.5 s.
- A 15 s or longer real-room trace with a surviving player in rooms 4–5, so no real-room cap-delay alignment and no cue overlap check beyond about 6 s.
- A spitter being killed, and the gap in rooms 4–5 with one spitter left.
- A dash through a shot, and the invulnerable-contact behavior with the dash.
- `run_play`, `run_tests` and `run_bots` were not run.
- Code-level causes (hypotheses are labelled as hypotheses).
- Exact lateral misses for each shot were derived, not read from a trace of the shot position.

## Open questions

- For `game-designer`: should a shot that touches an invulnerable player (dash or hurt) be removed, or keep going and hit once the window ends? Same question applies at a lesser scale to lunges.
- For `game-designer`: is two cues starting together after a cap delay acceptable in room 3 and practice rooms?
- For `studio`: if a real-room check is wanted before 0.6, a reaction-rule script that dodges (as in the manual's example) in rooms 4 and 5 for 15 s or more would give the trace. I did not use my last run on it.

## Expected output

Studio routes findings 7 and the room-3 simultaneous-start question to `game-designer`. Handoff 27's room 4–5 items can be treated as explained by the 0.5 spec (0.2 s lock gap, cap alignment, unconsumed shot), pending the step 35 build.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/34-studio-to-qa.md
