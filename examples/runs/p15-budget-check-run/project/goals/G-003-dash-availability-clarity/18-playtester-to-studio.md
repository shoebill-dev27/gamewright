---
kind: handoff
goal: G-003
seq: 18
from: playtester
to: studio
stage: Route
outcome: done
---
# 18: playtester → studio — Observation report: movement and dash in fights, 60 and 30 FPS

## Task

Read the player-side observation report below and route it. Experience issues go to the game-designer and defects to QA.

## Context

Goal G-003 (dash availability clarity). Handoff 16 asked me to play the current build (0.6-g002-public-32) as a player, using only the game's output and `repo/manual.md`. The focus was how I use movement and dash during fights and what I can tell about my options at each moment. I played mainly at 60 FPS and ran one session at 30 FPS.

## Findings

### Method

- I played by input automation only: a written script run through `python3 play.py --view player {script}`. I did not play live.
- I did not use the trace view and did not read source, tests or design documents.
- The same script ran twice, once with `fps 60` and once with `fps 30`. Each was a normal run (`mode run`) that started in room 1.
- Only room 1 was seen. I never cleared it, so I never saw rooms 2–5 or the boss.
- Timed inputs and the three reaction rules were fixed in advance. I did not adapt to the screen mid-run. When a grub reared back, my script did not dodge it on purpose. That means this report says nothing about how dodging with the dash feels in practice.
- Scripts used, identical except for the `fps` line:

```text
mode run
fps 60            # second run: fps 30
limit 40
driver-limit 45
0 move left
0.5 stop
1.0 dash right
1.5 dash right
2.0 move up
2.5 stop
2.5 attack
3.0 dash left
3.9 dash left
4.5 attack
5.0 move right
6.0 stop
6.0 dash up
when see g within 3 then face
when see r within 1.4 then attack
when see * coming within 1.5 then move aside
```

### Session summary

- Both runs ended in death in room 1, at 11.417 s (60 FPS) and 11.033 s (30 FPS).
- Each run had 3 hits ("hits": 3) and 2 swipes ("attacks": 2). Both swipes were "you swipe: miss". No enemy was ever defeated.
- The room started with three grubs (`g`). They kept coming and lunging, and I was hit once about every 1.3–1.7 s once they reached me in the top-left corner.

### What the dash display showed (concrete moments)

1. **Status line.** Every picture ended with `dash: ready`, `dash: active` or `dash: 0.4 s`. I could read my dash state at a glance in every picture.
2. **Dash used.** At 1.0 s I got `you dash right — usable again in 0.9 s`. The next picture, at 1.017 s, showed `dash: active`.
3. **Early dash refused.** At 1.5 s, 0.5 s after the dash started, I pressed dash again and got `dash not ready — 0.4 s left`. The picture showed `dash: 0.4 s`. I understood immediately why nothing happened.
4. **Dash ready message.** The game printed `dash ready` and a picture at the moment it returned.
   - At 60 FPS this was 1.850 s, 0.85 s after the dash.
   - At 30 FPS this was 1.900 s, 0.90 s after the dash.
   - The dash message says "usable again in 0.9 s" at both frame rates, but at 60 FPS the real wait was 0.85 s. I did not notice the difference during play.
5. **Chained dashes.** A second dash 0.9 s after the first worked at 60 FPS (3.0 → 3.9, with `dash ready` at 3.850) and at 30 FPS (3.0 → 3.9, `dash ready` at 3.900, same instant as my press). I did not try timings between 0.85 and 0.9 s, so I can't say where the edge feels.
6. **Countdown steps.** Later pictures counted down in tenths, for example `dash: 0.4 s` at 4.417 and `0.3 s` at 4.517 after a dash at 3.9, then `dash ready` at 4.750. Between half-second pictures I only knew the time from the last picture, as the manual says. The exact return was always announced.
7. **Dash end.** I saw `dash: active` only in the picture right after a dash started. There was no separate message when the dash ended.

### Dodging with the dash

- At 3.0 s a grub reared back about 10 tiles to my right, with a line pointing at me and 0.5 s to the lunge. I dashed left, and no hit followed.
- At 3.9 s another grub had 0.10 s left on its warning, with a line pointing up and right. I dashed left, and no hit followed.
- I cannot tell from the output whether the dash or the distance was what saved me, because no lunge message or picture appeared.
- All three hits came from lunges I did nothing about. My script did not use the dash in those moments, so I can't say if I could have dodged them.

### Where I was unsure or confused

- **Dash count after a hit.**
  - After each hit the status line showed a dash countdown. At 8.750 s it read `dash: 0.3 s`, then 0.2, then 0.1, then `ready` at 9.517 s.
  - I had not used the dash since 6.0 s, so it should have been ready.
  - The manual explains this as hit-stun, but on screen it looks like a cooldown. No `dash ready` message appeared afterwards. I would not know from the screen alone that this was hit-stun and not a spent dash.
  - It happened after all three hits at 60 FPS and after the two non-fatal hits at 30 FPS.
  - Impact: moderate. In the moments right after a hit, when I most want to escape, the display told me the dash was unavailable for a reason it did not give.
- **"(nothing happens)" lines.**
  - After a hit I got two `(nothing happens)` lines at the same time (for example 8.850 and 9.000 s, and again at 10.200 and 10.350 s).
  - They gave no reason and no mention of dash or of what was refused.
  - I do not know which action they came from. They appeared at the same time as my reaction rules were active. Impact: minor to moderate, because they were unexplained noise in the middle of a fight.
- **Grub warning timing.** The cue showed `0.50 s to the lunge` on the first picture, and the line pointed at where I stood. The warning is short, and pictures only come when the warning starts and every half second. So the later countdown (for example `0.12 s to the lunge`) was usually already stale when I read it. I could not tell, from the pictures, how late was too late for a dash.
- **Guessing.** I had to try the early dash at 1.5 s to find out whether the dash worked in the ready window. I did not need to guess about the display of ready versus active.

### Positives

- The `dash: ready / active / N s` field was always there, and the numbers matched the announced return times.
- The refusal text `dash not ready — 0.4 s left` told me exactly how long to wait.
- `dash ready` was announced at the exact moment, which I could rely on instead of the half-second pictures.

### Not observed

- Live, adaptive play: dodging on purpose with the dash, and the dash against a runner, a brute, a spitter or the boss.
- A swipe that hit or cancelled a grub, and any kill.
- Dash status on the clear or end screens (the manual says there is none).
- Any gamepad play. The script format cannot show how the dash feels on a pad.
- The edge between 0.85 and 0.9 s at 60 FPS.
- How the 60 versus 30 FPS dash timing feels during real play. All I have are the printed times.

## Decisions already made

None.

## Constraints

- Everything above is what a player could see in the game's output and the manual. I did not guess at causes or at how the game is built.
- The runs were scripted and non-adaptive, so impressions of feel are limited to what the text showed.

## Open questions

- Should the post-hit refusal (hit-stun) be shown differently from a spent dash? The status line shows the same countdown for both.
- Should the unexplained `(nothing happens)` lines be explained? They appeared in the same moments.
- A further session with reaction rules that dash on a warning (for example `when text "rears back" then dash aside`) would show whether the dash works as a dodge. I did not run one.

## Expected output

Route the experience points (hit-stun shown as a dash countdown, unexplained `(nothing happens)`, stale countdown numbers) to the game-designer. If the `(nothing happens)` lines are judged a defect, route that part to QA. The next step is the Studio's call.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
- Previous handoff: goals/G-003-dash-availability-clarity/16-studio-to-playtester.md
