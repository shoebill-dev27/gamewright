---
kind: handoff
goal: G-001
seq: 53
from: playtester
to: studio
stage: Play
outcome: done
---
# 53: playtester → studio — Observation report: combat in rooms 2–5

## Task

Report what I experienced playing the combat of rooms 2, 3, 4 and 5 as a player, with the scripts I used and the moments I describe.

## Context

This follows handoff 51, a fresh playtest of the build in `repo/`. I played with the player view only, with no trace view, bots or tests, and I did not read the source. I was told nothing about what changed.

I played as the profile: an action player who likes dodging and spacing, wants short intense runs and uses a gamepad.

## Findings

### Method

- I could not play live. I played by input automation with reaction rules, using `python3 play.py --view player {script}` at 60 FPS.
- The rules were reaction-time style: step aside from a shot coming at me, dash or step aside on "rears back" or "takes aim", swipe whatever is within about 1.4 tiles, and move toward or away from enemies.
- I did not use frame-perfect inputs. My feel notes come from reading the printed room pictures and cue lines, not from controller feel.
- Several runs were cut off by the output limit, so I only saw the first 20–24 s of the round 1 runs:
  - room 2 aggressive, up to about 24 s;
  - room 3 cautious, up to about 22 s;
  - room 4 aggressive, up to about 19.5 s;
  - room 5 aggressive, up to about 21 s.
- I never saw how those four runs ended.
- Runs seen in full:
  - room 2 cautious, 16 s;
  - room 3 aggressive, which cleared the room in 10.4 s;
  - room 4 cautious, 16 s;
  - room 5 cautious, where I went down at 9.0 s.
- I tried an aggressive and a cautious approach in every room.
- I did not try slow, deliberate play with long waits in any room.

### Scripts played

Round 1:
- room 2 aggressive:
  ```
  room 2
  when see * coming within 1.5 then move aside
  when text "rears back" then dash aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see g within 4 then move toward
  ```
- room 3 cautious:
  ```
  room 3
  when see * coming within 1.5 then move aside
  when text "rears back" then dash aside
  when see r within 1.4 then attack
  when see G within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 3 then move away
  when see g within 3 then face
  ```
- room 4 aggressive and room 5 aggressive used the same script:
  ```
  room N
  when see * coming within 1.5 then move aside
  when text "rears back" then dash aside
  when text "takes aim" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 1.4 then attack
  when see s within 1.4 then attack
  when nothing within 2 then move toward
  ```

Round 2, all with `end 16`:
- room 2 cautious:
  ```
  room 2
  end 16
  when see * coming within 1.5 then move aside
  when text "rears back" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 1.4 then attack
  when see G within 3 then move away
  when see r within 3 then move away
  ```
- room 3 aggressive:
  ```
  room 3
  end 16
  when see * coming within 1.5 then move aside
  when text "takes aim" then move aside
  when see s within 1.4 then attack
  when see s within 12 then move toward
  ```
- room 4 cautious:
  ```
  room 4
  end 16
  when see * coming within 1.5 then move aside
  when text "rears back" then move aside
  when text "takes aim" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see s within 1.4 then attack
  when see g within 3 then move away
  when see r within 3 then move away
  ```
- room 5 cautious:
  ```
  room 5
  end 16
  when see * coming within 1.5 then move aside
  when text "rears back" then move aside
  when text "takes aim" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 1.4 then attack
  when see G within 3 then move away
  when see g within 3 then move away
  ```

### Session summary

| Run | Result I saw |
|---|---|
| Room 2 aggressive | 3/3 hearts until 11.6 s. Hit once by the brute's lunge, then 2/3 until the output cut at about 24 s. Runners and a grub killed, room not cleared. |
| Room 2 cautious | Hit by a grub at 4.25 s and 5.4 s, so 1/3. Stalled for 10 s, kiting the brute along the left wall. Ended at 16 s with the brute alive. |
| Room 3 cautious | Hit by shots at 3.9 s and 4.7 s, so 1/3. Then a long standoff with shots filling the room, no kills, until the cut at about 22 s. |
| Room 3 aggressive | Cleared at 9.4 s with 2/3 hearts. One hit by a shot. All three spitters killed. |
| Room 4 aggressive | 3/3 hearts until the cut at about 19.5 s. Two grubs/runners hit or killed, spitters untouched. |
| Room 4 cautious | Hit by a shot at 4.8 s and by a grub at 14.7 s, so 1/3. Two kills, ended at 16 s with enemies left. |
| Room 5 aggressive | Hit once by a shot at 4.35 s. Then 2/3 through about 21 s. Two grubs and one spitter killed, brute still alive. |
| Room 5 cautious | Went down at 9.0 s. Hit by shots at 4.3 s and 6.4 s, then by a grub lunge. |

### Concrete moments

- **Room 3 opening, 1.2 s.** "A spitter takes aim" printed, and a big `~` line crossed the whole room through me. It was very readable: I knew where the shot would go and how long I had (0.6 s). I felt in control.
- **Room 3 cautious, about 9.6 s onward.** All three spitters took aim at the same instant, three times in a row (9.6 s, 13.8 s, 17.4 s and again at 19.8 s). Lines crossed the screen and I could only slide along a wall and wait. My attention dropped. It felt like waiting out a pattern, and I never had a way to fight back.
- **Room 3 aggressive, 1.2–9.4 s.** I charged the spitters and swiped them as I reached them. This felt completely different from the cautious run: quick, tense, over in about 10 s. It was the most fun combat of the session. I took one hit at 2.1 s when I walked into a shot that was already flying.
- **Rooms 4 and 5, spitters.** The spitters alternated about every 0.6–0.8 s and it was always the same rhythm: aim, glow, spit, then the other one. Stepping aside worked every time I reacted on the cue. The shots I took (4.35 s in room 5 aggressive, 4.27 s and 6.43 s in room 5 cautious, 4.78 s in room 4 cautious) were ones where I was already standing in the line. I could see them coming, so these were fair hits.
- **Grubs and runners.** "A grub rears back" printed for every grub, runner and brute alike. I could only tell them apart from the `cue:` line, which says "r", "g" or "G". Because I dashed on the message alone, I often dashed away from a runner that was far off and wasted a dash. Dashing "aside" on every cue left me dashing about every second in room 2 (about 12 dashes in 24 s) and landing few swipes.
- **Room 2 cautious, 4.0–4.25 s.** A grub reared back with a 0.5 s warning. I swiped at the last moment (0.05 s left) and was hit anyway. The swipe did not stop it. This felt unfair, though the pictures show I was close, so I may have mistimed it. The manual says a swipe within 1.5 tiles cancels, and this one did not.
- **Room 2 cautious, 5.0–5.4 s.** I swiped a runner and killed it, then was hit by a grub at 5.4 s with no new warning that I saw. It was probably another lunge that started right after, but I did not see its cue in the print. This one felt like damage I could not see coming. I am not certain.
- **Room 2 aggressive, 10.9–11.6 s.** The brute reared back with a 0.7 s warning and I stood in the line for the whole time. I got hit at 0.08 s left. The warning was long and obvious, so this was my own mistake. Brutes on their own are slow and easy to step away from.
- **Room 2 cautious, 6–16 s.** I backed away from the brute along the left wall and nothing happened for 10 s. The brute crept after me without attacking. Boring.
- **Room 5 cautious, 8.35–9.03 s.** A grub reared back at 0.5 s warning. I swiped it once (hit) at 8.93 s, and the grub lunged and hit me at 9.03 s, taking my last heart. I think I stayed in the lunge line because the grub needed two swipes. This felt harsh: I did the "right" thing (swipe to cancel) and still went down. I could not tell whether the swipe was supposed to have stopped it.
- **Room 5 aggressive, 6.2–8.0 s.** Grubs and the brute were near each other. I got a good hit streak: "grub hit, brute hit", then "grub defeated, brute hit". It felt busy and fun for a moment. I also dashed to avoid a brute lunge at 7.35 s and it worked. The brute's lunge cue came while I was swiping grubs, and I had to choose between the two. That was the one moment in rooms 4–5 where I had to decide something.
- **Nothing looked broken.** No crash, no stuck state and no shot from nowhere. Every hit I took had a visible cue before it, except possibly the 5.4 s hit in room 2 noted above.

### Issues with impact

1. **Rooms feel alike, high impact.** Almost every threat is the same move: see a cue, step or dash sideways, swipe afterwards. Grub, runner and brute differ in warning time (0.5 s, 0.35 s, 0.7 s) and in swipes needed, but I answered all of them the same way. Spitters in rooms 3, 4 and 5 are the same too. By room 4 I felt I had already seen it all. "I never needed to think about which enemy it was."
2. **The fighting-style difference is only visible in room 3, medium impact.** In room 3 charging and kiting felt very different. In rooms 2, 4 and 5 both approaches ended up as the same cue-dodging loop. The cautious runs mostly burned time and lost hearts, and the aggressive ones did not feel riskier.
3. **Cautious play stalls, medium-high impact.** In room 2 cautious (10 s of nothing) and room 3 cautious (several simultaneous volleys with no way to progress), I spent a lot of time waiting. Kiting a brute along a wall was dull.
4. **Simultaneous spitters in room 3, medium impact.** Three lines at once across the whole room were readable but left me with only one answer: slide along a wall.
5. **Dash was nearly free, medium impact.** Dashing on each cue avoided nearly all damage, so threat felt low in room 5 aggressive and room 4 aggressive (3/3 at the cut). Hits came almost only when I did not react.
6. **Same message for every lunger, low-medium impact.** "A grub rears back" is printed for runners and brutes too. I could not tell from the message which one was about to hit me.
7. **Swipe versus lunge timing, medium impact.** The two hits where I swiped a rearing grub and was hit anyway (room 2 cautious at 4.25 s, room 5 cautious at 9.03 s) felt unfair, because I could not tell whether swiping that late would work.

### Positives

- Spitter telegraphs are very readable: the line, the brightening and the 0.6 s countdown. I never felt cheated by a shot.
- Grub and brute warnings are clear, and the brute's long warning makes it feel heavy.
- Room 3 aggressive was the best moment: fast, tense and clean.
- Room 5's mix of grubs, brute and spitters at 6–8 s was the most interesting crowd.
- Runs are short, which fits the profile.

## Decisions already made

None.

## Constraints

- I used the player view only, with no trace view, bots or tests.
- I did not read source code.
- This report contains only what I saw and did, with no guesses at implementation and no code changes proposed.
- Four round 1 runs were truncated in the output, so I report nothing about how they ended.

## Open questions

- Does a swipe at a rearing grub cancel it when done very late (under about 0.1 s)? Twice I swiped and was hit anyway, and I could not tell why.
- What caused the grub hit at 5.4 s in room 2 cautious? I saw no cue before it.
- I did not try slow, waiting-style play or other dash timings in any room, and I did not play room 1.

## Expected output

This report goes to `studio`, for routing. Experience issues belong with `game-designer`. The possible unfair-hit moments might go to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/51-studio-to-playtester.md
