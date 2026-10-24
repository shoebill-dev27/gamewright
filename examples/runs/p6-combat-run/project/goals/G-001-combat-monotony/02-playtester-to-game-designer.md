---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 02: playtester → game-designer — Observation report: combat in rooms 1–3 of build 0.4

## Task

Use this player-side report to diagnose why combat feels the way it does. Rooms 4 and 5 were not played (see Method).

## Context

The studio asked for a first-hand account of combat across several encounters. This report comes from the player view only. I did not read the trace or the source.

## Findings

### Method (what I actually did)

- I played with input automation: one pre-written timed script per room, run through `python3 play.py --view player`.
- I could not react to what happened on screen. Each script was fixed in advance. I had one run each of room 1 (20 s), room 2 (25 s) and room 3 (30 s).
- I did not play rooms 4 and 5 or the practice room, so I know nothing about them.
- I cannot speak to feel in the sense of hands on a gamepad. The impressions below come from the half-second snapshots and the event log.
- My scripts were generic: swipe, step, dash, repeat, aimed at where enemies seemed to be. A human reacting live would do better than I did, so deaths here show less about difficulty than about how the enemies behave.

### Session summary

| Room | Enemies | Outcome | Time of death | Swipes landed |
|---|---|---|---|---|
| 1 | 3 grubs | Died, 0 kills | 3.6 s | 0 of 5 |
| 2 | 4 grubs | Died, 0 kills | 4.6 s | 1 of 6 (a "grub hit" at 4.5 s, but the grub didn't visibly die; 4 still alive at the end) |
| 3 | 3 spitters | Died, 0 kills | 18.9 s | 0 of about 17 |

### Concrete moments

**Room 1 (grubs)**
- The grubs drifted toward me slowly and steadily. I mostly swiped at empty air at 0.5 s. I walked right, and by 2.0 s a grub was next to me.
- I got hit at 2.03 s, 2.83 s and 3.63 s. That is one heart about every 0.8 s while a grub stayed adjacent. I was standing beside it and could not shake it off.
- My inputs were ignored right after each hit. A swipe at 2.1 s and a move at 3.0 s gave "(nothing happens)". It felt like a short lockout of roughly 0.1–0.3 s after being hit, which stops me from hitting back or escaping.
- After "you went down", the grubs just stood next to my body for the rest of the session (about 16 s of identical frames). Nothing prompted a restart.

**Room 2 (more grubs)**
- It was the same fight with one more grub. They drifted in from the corners and closed in with no real variation.
- I took hits at 3.0 s, 3.8 s and 4.6 s, and died at 4.6 s. Inputs after hits were swallowed again (3.0, 3.1 and 4.0 s).
- The only hit I landed was a swipe at 4.5 s ("grub hit"). The grub count didn't drop, and I couldn't tell whether it was damaged. There was no visible reaction in the snapshots.

**Room 3 (spitters)**
- This is a different enemy type, and it felt different at first. The spitters sit in fixed spots (two at the bottom corners, one top-left) and never moved. I never saw them approach, retreat or reposition.
- All three spit at exactly the same moment, every 2.0 s on the dot. Each volley fills the room with slow shots. Dodging between them felt like threading a pattern rather than fighting something.
- I survived about 19 s, longer than the grub rooms. Hits came at 9.47 s, 16.9 s and 18.9 s.
- After I went down, the shot pattern repeated unchanged every 4 s (the same positions again and again). It looks like a loop, not something reacting to me.
- The screen was cluttered with `*` most of the time, and a swipe at a spitter was never in range. I never found a safe moment to close in on a spitter. I can't say whether that is possible.

### Over time and between encounters

- Rooms 1 and 2 felt essentially identical. Slow enemies walk at you, touch you, you lose hearts, and you go down in about 4 seconds. Only the count changed (3, then 4).
- Nothing evolved within a fight. The grubs didn't change speed, wind up, telegraph or vary their approach.
- Room 3 changed the threat from touch to projectiles, but it kept the same two traits: enemies are predictable and they never change what they do.
- Over three rooms I saw no new behaviour from any enemy after the first few seconds.
- My attention dropped in the grub rooms. After the first contact there was little to read or decide, and I was mostly waiting to be touched. It spiked briefly in room 3 when a volley came my way.

### Issues with impact

1. **Grubs feel samey and unavoidable (high).** They are slow, but I was caught within about 2 seconds, and then I took a heart every 0.8 s. I never felt a spacing or dodging decision. That doesn't fit an action player who likes spacing.
2. **Input lockout after being hit (medium).** Swipes, dashes and moves right after a hit did nothing, so the best moment to escape or counterattack is lost.
3. **Unclear hit feedback on my attacks (medium).** The one landed swipe showed no visible effect and the grub count didn't change. I couldn't tell if it was working.
4. **Spitter volleys are rigid (medium).** Exactly synchronized, exactly timed, never moving. Fine to learn once, but it looks the same every time.
5. **Little variety across rooms 1–3 (high for the goal).** The sense of monotony comes from enemies that never change what they do, not from the number of enemies.

### Possibly broken (separate items)

- **After death the session just runs on.** There is no game-over, restart or any change except enemies standing still. This may only be a feature of the scripted play.
- **The grub I hit in room 2 stayed in the enemy count** (4 left at the end). I can't tell whether grubs need several hits or the hit didn't register. A player would call this confusing.
- **Inputs ignored right after a hit** (see above). It might be deliberate hit-stun, but it was not communicated.

### Positives

- Room 3 gave me the one stretch of tension: reading the shots and dashing through gaps.
- The two enemy types look clearly different on screen, and the room is easy to read.

### Player suggestions (my opinion as a player, not a code change)

- Give enemies something to react to: a wind-up before touching me, a pause after hitting, or a different approach path.
- Show clearly when my swipe hits (flash, knockback, sound).
- Make spitters move or stagger their shots so volleys aren't identical.
- Make it clearer when I'm stunned and for how long.

## Decisions already made

None.

## Constraints

- Observations come only from the player view and three scripted runs, not from live play.
- Rooms 4 and 5 are not covered. If the designer needs them, ask the studio for another play round.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001). Any option you propose must stay inside that.

## Open questions

- Do rooms 4 and 5 behave differently? I did not see them.
- Is the hit lockout intended? Does a grub need more than one swipe? I could not tell from the player view. Compare these with `design/combat.md`: if the document says the behavior should differ from what was observed, treat it as a defect and hand that item back to the studio for `qa` (Observe) instead of diagnosing it as a design cause.

## Expected output

The game designer reads this report and does the Diagnose step (`diagnose-experience`): identify the causes of the combat sameness in design terms and give solution options, with your recommendation and the cost and risk of each. Put the diagnosis in Findings of the outgoing Handoff.

- If the options are a real choice of direction, priority or scope, or one touches the vision or D-001, address the result to `game-director` (Decide).
- If the options are all within your authority and the vision, say so, decide, and hand to the next step per your Role contract.
- List any items that look like defects (see Open questions) separately, and say whether rooms 4 and 5 need another play round.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
