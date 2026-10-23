---
kind: handoff
goal: G-003
seq: 10
from: playtester
to: studio
stage: Route
outcome: done
---
# 10: playtester → studio — observation report on build 0.6 (dash readiness, rooms 1 and 3)

## Task

Route this observation report. It covers what a player sees of dash readiness and early fighting in build 0.6. Experience issues go to game-designer and defects to qa, at the Studio's discretion.

## Context

The Studio asked for a play session of the current build from the player view and `repo/manual.md` only, paying particular attention to dash. I read no source, tests, design documents or other handoffs, and I did not use the trace view. I was given no expected result.

## Findings

### Method

- I played by input automation: written scripts run with `python3 play.py --view player`. I did not play live and I did not use a gamepad.
- I ran three sessions, all in the player view:
  1. Room 1 at 60 FPS (`room1-dash-60`).
  2. Room 1 at 30 FPS (`room1-dash-30`), the same script as session 1.
  3. Room 3 at 60 FPS (`room3-dash-react-60`).
- Sessions 1 and 2 used timed dashes at 1.0 s, 1.3 s and 2.0 s, a move left at 2.5 s, and reaction rules that attack grubs within 1.4 tiles and move toward grubs within 3 tiles.
- Session 3 used timed dashes at 0.5 s, 0.8 s and 1.2 s, plus these reaction rules:
  - `when text "dash ready" then dash aside`
  - `dash aside` when a projectile is coming within 1.5 tiles
  - attack grubs and runners that are close
  - move toward spitters and grubs

### What I did and saw

**Session 1: room 1, 60 FPS (ended at 5.53 s, room cleared, 3/3 hearts)**
- The line above the room read `dash: ready` from the start.
- At 1.000 I dashed left. The game printed `you dash left` and `dash recharging: ready again in 0.85 s`. The line then read `recharging 0.72 s` at 1.13 s and `0.35 s` at 1.50 s.
- At 1.300 I pressed dash again and the game printed `dash not ready: 0.55 s left`. Nothing happened, and the dash was not used later on its own. 1.85 − 1.30 = 0.55, so the number was right.
- `dash ready` was printed at 1.850, exactly 0.85 s after the dash. The 2.000 dash worked, and the next `dash ready` came at 2.850.
- The countdown on the line and the messages agreed with each other throughout.
- Fighting: grubs reared back, and the `~` line and `cue:` line appeared each time. I cancelled two lunges by swiping (`grub hit`) and defeated four grubs. I took no damage.

**Session 2: room 1, 30 FPS (ended at 5.87 s, room cleared, 2/3 hearts)**
- Dash behaved the same way: the same messages, `dash not ready: 0.57 s left` at 1.3 s, and `dash ready` at 1.900 and again at about 2.9 s.
- At 30 FPS `dash ready` came about 0.05 s later than at 60 FPS: 0.90 s after the dash instead of 0.85 s. At 1.50 s the line said `0.37 s` left, which points to 1.87 s, but the message appeared at 1.900. This is below one frame and I did not feel it, but the printed "ready again in 0.85 s" was not exactly what happened at 30 FPS.
- At 1.667 the game printed `the grub's lunge had already started, the swipe was too late to stop it`. At 60 FPS the same swipe came at 1.617 and cancelled the lunge. The message was clear.
- At 3.100 I was hit by a grub, down to 2/3. The line changed to `recharging 0.30 s` and read `ready` again by 3.50 s. This matches the manual: after a hit I cannot dash for a moment, and the line shows it.
- I had no dash rule here and the dash was ready at 3.0 s. I walked into a lunge I could have dashed through, so that hit was my own script's fault.

**Session 3: room 3, 60 FPS (died at 12.0 s, 0/3 hearts, 3 enemies left)**
- Pressing dash early at 0.8 s printed `dash not ready: 0.55 s left`. Pressing at 1.2 s printed `0.15 s left`, which was correct against `dash ready` at 1.350.
- Neither early press was saved for later. The next dash was my rule firing on `dash ready` at 1.350, which fits "not saved for later".
- The `text "dash ready"` rule fired on every `dash ready` message, so dashes happened exactly every 0.85 s. Reading the line and the `dash ready` text was enough to time dashes.
- Room 3 has three spitters and a grub. The spitters often aimed together, at 6.4 s, 8.8 s and 11.4 s, and all three spat at the same moment (7.0, 9.4, 12.0). With three overlapping `~` aim lines I found it hard to tell which line was dangerous.
- The cue lines helped (brightness and seconds left per spitter). I was hit by shots "from the west" at 8.133 and 10.833, each time between dashes (the line read `recharging 0.15 s` and `0.50 s`).
- My "dash aside" reaction does not choose a safe side well. Dashing often did not get me off a line, and I could not tell what "aside" meant in a room with three crossing lines.
- At 11.5 s I walked next to a spitter (`sP`). At 12.0 s it spat and I was hit in the same instant ("from the west"), which ended the run. I do not think I could have reacted to that.

### Moments I could not observe or was unsure about

- I never saw a shot or lunge meet me during a dash, so I did not confirm that dashing really makes me unhurtable. The manual says it does; my sessions did not exercise that moment.
- I did not see the 0.25 s dash length directly. The pictures are every 0.5 s or on events. I only saw the player end up in a new place.
- I did not check whether the dash distance is the same at 30 and 60 FPS.
- I did not reach rooms 2, 4 or 5 or the boss, and I did not use `mode run`.
- I cannot say anything about gamepad feel or about how the text readout compares with a real-time display. In text form, the countdown on the line is easy to read.
- After a hit, the line shows `recharging` but gives no message that I am briefly invulnerable. The manual mentions "still flashing after a hit", but the display did not show that to me.

### Issues, with impact

1. **Room 3 felt crowded and hard to read.** Three spitters often aimed and spat in sync and the `~` lines overlapped, so I could not tell which lane to leave. Impact: high for a short, intense run. I died here at 12 s without feeling I had a real choice.
2. **Printed cooldown and actual ready time differed slightly at 30 FPS.** The game said 0.85 s and the dash came back at 0.90 s. Impact: very low, noticeable only when comparing the numbers.
3. **A dash used "blind" (reaction rule firing the moment it comes back) does not protect me.** The dash comes back every 0.85 s but there is no gap long enough to be safe from three shots. This is about my own rule, not a game fault. Impact: medium. It shows that being able to dash is not the same as dashing at the right moment.

### Positives

- Dash readiness was very clear. The `dash: ready` / `recharging N s` line, the `dash recharging: ready again in 0.85 s` message, the `dash not ready: N s left` refusal and the `dash ready` message agreed with each other in every case.
- Refused presses told me what was wrong and by how much, and nothing happened. Presses were not queued, as the manual says.
- Warnings in room 1 were readable and fair, and the "swipe too late" message explained a missed cancel.

### Open player questions

- How long am I protected after a hit, and can I see it?
- Do 30 FPS and 60 FPS give exactly the same dash cooldown?
- What does "dash aside" pick when several lines cross?

### Reproduction

- Sessions 1–3 above used the scripts exactly as written (room 1 or room 3, `fps 60` or `fps 30`, `end 20` or `end 30`; the timed dashes and rules are listed under Method). The 30 FPS grub-lunge difference is at 1.267 to 1.667 s in session 2.
- The death in session 3 is at 11.5–12.0 s.

## Decisions already made

None.

## Constraints

- All observations come from the player view and `repo/manual.md`. Nothing here comes from source, tests, design documents, other handoffs or the trace view.
- Observations come from scripted play, not gamepad play. What the dash feels like in the hand is not covered.
- Only rooms 1 and 3 were played.

## Open questions

- Should another playtest session cover rooms 2, 4 and 5, and a moment where a dash meets a lunge or shot, so that dash invulnerability can be observed?
- Should the 30 FPS 0.85 s vs 0.90 s difference go to qa?

## Expected output

The Studio's Route operation sends the experience issue (room 3 readability) to game-designer and the possible 30 FPS cooldown difference to qa, or asks for another play round on the unobserved parts.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: goals/G-003-dash-readiness/10-playtester-to-studio.md
- Decisions: none
- Previous handoff: goals/G-003-dash-readiness/09-studio-to-playtester.md
