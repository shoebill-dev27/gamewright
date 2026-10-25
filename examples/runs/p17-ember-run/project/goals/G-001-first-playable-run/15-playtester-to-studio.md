---
kind: handoff
goal: G-001
seq: 15
from: playtester
to: studio
stage: Review
outcome: partial
---
# 15: playtester → studio — playtest report: seed 42, floor 1 only (about 16 turns)

## Task

Read the observation report in Findings. It covers a very short slice of play. Decide whether more play is needed before judging the game's feel.

## Context

I was asked to play the Ember Hollow build as a player, using only the manual, and report what I experienced. I used one batch of runs, played through scripts only. I did not reach the end of a run, and I saw only a small part of the game.

## Findings

### Method (what I actually did)

- I played through text scripts with `node play.js`. This was input automation, not live play. I could not react turn by turn within a script, only between batches.
- I used seed 42 only, in two scripts: one walking east and south around the start room, and one walking west for 16 turns.
- I could not open a browser, so I know nothing about `index.html`, mouse play, or how the page looks or feels.
- I did not use trace or internal-state output.
- I played no other seeds, never got past floor 1, and had no win or loss. My longest run was 16 turns.

### Session summary

- The start room is a closed 5×5 room with the way out to the west. I first walked east and south to look around, and found only walls.
- On the second script I went west along a corridor and met one cave moth. I fought it and killed it, ending at HP 11/12 and Ember 84/100 on turn 16. A lone unlit brazier (`B`) came into view far to the west, and I did not reach it.

### Concrete moments

1. **Start (turn 0).** I could tell where I was, and the frame was readable: floor, HP, ember bar, and "dims 1/turn". The `<` appeared on the tile I started on only after I moved off it. That is fine, but it was a small surprise.
2. **Bumping walls (turns 2–3 of the first script).** The frame is printed again with "(refused: no turn passed)". I understood at once that nothing was spent. This is clear and a relief.
3. **Stale messages.** The message "You descend into Ember Hollow with one ember." stayed at the bottom of the list through every frame. Later, "The cave moth hits you for 1 / You hit the cave moth for 2 / The cave moth dies" was repeated in the next three frames, long after the moth was dead. Because of this I couldn't tell from the list whether something had just happened or was old. After the kill I briefly wondered whether the moth was still hitting me. HP stayed at 11, which showed it was not. Impact: low to medium. It makes the event log hard to trust at a glance.
4. **The moth appears (turn 9).** A moth `m` showed up at the edge of sight, about 6 tiles west. The creature list said "hunting" with its position. It closed in one tile per turn while I kept walking toward it.
5. **The warning (turn 11).** The moth was two tiles away. A `?` appeared on the tile between us, and the line read `Danger: W (m)`. I could tell what would hurt me if I stepped there. I stepped there anyway to test it, and on turn 12 the moth hit me for 1 (HP 12 → 11). The warning was accurate. Once it was adjacent the frame marked it with `!` and "THREAT: hits for 1 at its next action".
6. **The fight (turns 12–13).** One attack killed the moth ("hit for 2, dies"). The fight was over in a turn and cost 1 HP. It felt trivial rather than tense, but this was one weak creature.
7. **Ember (turns 0–16).** Ember went 100 → 84, exactly 1 per turn. Walking, waiting and fighting all cost the same. I never saw the "2 per turn" drain, because I never got near a Gloom. I could not feel any light/time trade-off in 16 turns: no braziers reached, no items, no choice that cost ember beyond walking. Two waits in the first script cost the same as moving, which tells me waiting is never free.
8. **Map view.** The map scrolls with me, so the start room slid off to the right as I went west. Remembered tiles (`,` and `%`) showed where I'd been. I found this readable. The many blank lines under the map are a bit odd.

### Answers to the open questions

- **Could I tell what could hurt me next turn?** For the one moth I met, yes: the `?` mark, the Danger line, and the `!` threat line all agreed and were right. I can't say anything about hounds, shades or the Gloom.
- **Did the light and the passing of turns feel like a real trade-off?** I couldn't tell. In 16 turns of floor 1, with nothing pressing, the ember was just a slowly falling number. I don't know whether the 100 ember is generous or tight.
- **Was a run short and varied enough to want another?** I can't say. I did not finish a run, so I have no run length. My longest was 16 turns. Floor 1 on seed 42 started with an empty closed room, then a corridor and one moth, which felt quiet.
- **Anything broken?** I saw no crash or stuck state, and nothing contradicted the manual. The only oddity is the stale messages (moment 3), which look like a presentation problem, not a rule problem. One thing was not verified: after the moth died I did not see whether a dead creature's mark or list entry lingered. The frames showed "Creatures: none in sight", so I think it did not.

### Issues with impact

- Stale or repeated messages in the log. Impact: low to medium, confusing about what just happened.
- Nothing else observed.

### Positives

- Refused moves cost nothing and say so plainly.
- The danger warnings were accurate and easy to read.
- The frame is compact and quick to scan.

### What I could not observe

- Anything in the browser: keyboard, mouse, layout, colours, the page itself.
- Shades, hounds, the Gloom, items, lit braziers, stairs down, floors 2–5, winning, dying, other seeds.
- Whether runs are varied between seeds, and how long a full run takes.

## Decisions already made

None.

## Constraints

- I used only the manual and what the game printed. I read no source, tests or design documents, and used no trace output.
- I did not edit the build.
- This report holds only what I observed. Hypotheses are marked as such.

## Open questions

- Is a further play round wanted? It should cover several seeds, deeper floors, and reaching a brazier and an item. This round showed almost none of the game's tension.
- Should someone with a browser check `index.html`? I could not.

## Expected output

The Studio reads this report and decides on routing: experience issues to `game-designer`, defects to `qa`. The stale-message issue is the only candidate so far. It looks like a presentation defect.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: repo/manual.md; the build in repo/
- Decisions: none
- Previous handoff: goals/G-001-first-playable-run/14-studio-to-playtester.md
