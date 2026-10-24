---
kind: handoff
goal: G-001
seq: 38
from: playtester
to: studio
stage: Play
outcome: done
---
# 38: playtester → studio — Observation report: level 1 of build 0.6, played as a 7–10 year old

## Task

Report what a child player sees and does in level 1, from load to solved state.

## Context

This is the playtest requested in handoff 37. I played level 1 of `sim/build-0.6.md` as a child aged 7–10, an early reader, playing beside a parent.

## Findings

### Method (what I actually did)

- This was **not live play**. There is no device. I read `sim/build-0.6.md` as the player-visible description and stepped through it as the child would, using touch only.
- Every moment below is derived from that description. I did not see the screen, so I could not judge real visibility, real timing feel or how a real child's attention behaves. Where that matters I say so.
- I relied on the on-screen text only as much as a child who doesn't read would. I used no outside knowledge of the intended solution.

### Session summary

**Path A: child touches the pool first (most likely path, given what draws the eye).**

The level is solvable by touch alone. The pool is the one thing that pulses and has the dark outline, so I'd expect it to be the first thing I touch. I rate the path as clear and responsive. The one real gap is that I can't see what happens at the end.

**Path B: child taps the crab, home or sand first (a plausible detour).**

Every tap gets some response, but the responses are uneven. Some are strong and some are faint. Whether the child gets back to the pool from here is the part I'm least sure about.

### Concrete moments, in order (Path A)

1. **Load (0–1.6 s).** The pool slides about a quarter of the way toward the home and slides back, with no touch. I'd see something moving without being asked. It is short, and I can't tell whether I'd connect it to "the pool goes to the house". The text bubble "Drag the tide pool!" is there, but as an early reader I might ignore it.
2. **At rest (after 1.6 s).** The pool is blue and darker than the sand, with a dark outline. It pulses slowly, about 6% bigger and back every 2 s. The crab and home sit still with lighter outlines. Nothing else moves. This makes the pool look like the thing to touch, but the pulse is gentle. The description gives no sign of any extra nudge if I wait. Nothing happens on its own, so a child who doesn't act just sees a gently pulsing pool.
3. **Touch the pool.** It grows about 10% within 0.1 s and a dark shadow appears under it, which feels like picking it up. It follows my finger 1:1. This is a clear, immediate response and a good moment.
4. **Drag toward the home.** When the pool's center gets within about 1.5 pool-widths of the home, the home glows steadily. This is a helpful "you're close" cue. I would likely keep going once the house lights up.
5. **Drop on the home.** The level finishes. **I can't tell what a player sees or hears at the solve.** The description says only that the level is finished. I can't say whether it feels rewarding.

### Concrete moments (Path B: detours)

- **Tap the crab.** It flips to face the pool if needed and wiggles for 0.4 s. Then the pool does two quick bigger pulses (about 15%) over 0.6 s. This is lively and reads as the crab pointing at the pool, though I can't be sure a child would read it that way. It is a good response.
- **Tap the crab again soon after.** If it's within 1.5 s of the last pulse, I get the wiggle but no pool pulse. If I tap fast, pulses come only about every 1.5 s (three or four in 5 s). Some taps would feel less rewarding than the first.
- **Tap the home.** It brightens about 20% and fades over 0.6 s, and the pool pulses (same 1.5 s limit). It's a quiet response.
- **Tap empty sand.** If a pulse is allowed, the pool pulses and nothing else happens. If not, the pool gets a brief brightness flash (+15%, about 0.3 s) and nothing else. **This flash is the faintest response in the level.** On a real screen, in daylight or beside a parent, a child may not notice it and may feel the tap did nothing. I can't confirm this without a device. I flag it because this player loses interest quickly when nothing seems to respond.
- **Drop the pool on the crab.** The pool stays there and the crab does not react. This is a dead end with no feedback, and I'd wonder if I did something wrong or the game was stuck.
- **Drop the pool anywhere else.** The pool just stays where I put it, with no response. I'd pick it up again, but there is no sign of whether I'm closer or farther away except the home glow when near.
- **Touch the pool during the opening slide.** I can grab it where it is drawn, and it follows my finger. Touching where it started but isn't currently drawn goes to the sand instead. That would feel like a missed grab for a moment, but it is a very short window.
- **Reduce-motion devices.** The opening slide is skipped. The pool pulse is brightness-only and the crab only brightens, so the cues are subtler there. I didn't play that variant in detail.

### Issues and impact

1. **Unknown solve moment.** I couldn't observe what the solved state looks like, so I can't say whether the end is rewarding. Impact: unknown.
2. **Faint sand-tap flash.** It is a 0.3 s, +15% brightness change on the pool and could read as no response. Impact: medium, if it is as subtle as it sounds. Not verified on a device.
3. **Dead-end drops.** Dropping on the crab, or anywhere that isn't the home, gives no response. Impact: medium for a child who gets stuck there.
4. **No cue if the child waits or wanders.** Only the gentle pulse remains. Taps on the crab, home and sand can give less than the first tap did (the 1.5 s limit). Impact: low to medium.
5. **Reliance on the text bubble.** I didn't need it, and the pool's pulse and outline carried me, which I count as a positive. Early readers who miss the pool's cue have only the pulse.

### Positives

- The pool is clearly the odd one out: darker outline, bluer, pulsing.
- Picking it up is satisfying: it grows, it has a shadow and it tracks the finger.
- The home glow while dragging is a clear "getting close" cue.
- Every touch on the crab, home, sand or pool gets some response within 0.2 s.
- Crab wiggle plus pool pulse reads as a friendly hint.

### Could not observe

- The solved state and anything after the drop on the home.
- Real brightness, contrast and timing on a screen.
- Where a real child would actually hesitate. Hesitation points above are inferred from the description, not seen.
- A visible undo control. Undo is mentioned, but nothing says how a player triggers it.

## Decisions already made

None.

## Constraints

Observations only. I propose no fixes or design changes.

## Open questions

- What does the player see and hear when the level is solved?
- How does a player trigger undo?

## Expected output

This report goes to the Studio for routing. Experience issues would go to game-designer. If any defect is suspected, qa should confirm it on a device.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.6.md
- Decisions: none
- Previous handoff: goals/G-001-first-puzzle-stall/37-studio-to-playtester.md
