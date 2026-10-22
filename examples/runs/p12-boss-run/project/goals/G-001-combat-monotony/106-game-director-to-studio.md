---
kind: handoff
goal: G-001
seq: 106
from: game-director
to: studio
stage: Close (Next)
outcome: goal-met
---
# 106: game-director → studio — Review pass 4: goal met on the text-view build. The wording round closed the "player can tell why" clause. No Owner escalation. Close G-001 per D-013, with proposed Goals and one Owner item.

## Task

Route the Review result. The verdict is **goal-met**. D-014 records it. The Studio Closes the Goal.

## Context

G-001 (Owner: 「戦闘が単調なので改善したい」). Passes 1–3 returned goal-not-met. Pass 3 (92, D-013) found the variety half met and two holes in the "player can tell why" half: a shot hit named no source (A), and a late swipe gave no explanation (B). One wording-only round followed: Design 94 (corrected in 102), Build 96 (manual marker fixed in 101), Verify 98 (fail on the manual marker only), Verify 104 (pass). This pass is a paper check; I ran no `play` or `bots`.

## Findings

Evidence is compared with the success condition in `goal.md`, not with the plan.

### Half 1: different situations call for noticeably different play. Met (unchanged since pass 3)

- Runner, standard grub and brute ask different things (63, 88). Spitters ask a fourth. Rooms 4–5 combine them.
- Room 3 has a second ask (D-012).
- Nothing in this round touched a rule, number, timing, cap, cue or input (98 and 104 report the observed values match spec, and the suite is green). The variety half therefore stands as judged in 92.

### Half 2: the player can tell why. Now met

- **Hole A (shot-hit source) is closed.**
  - QA 98 W1 passed at both 30 and 60 FPS for all six placements: east, north, west, south, north-east and south-east.
  - W2 passed at 60 FPS in room 4 (1 hit) and room 5 (3 hits). Each direction word matched the reversed `cue:` direction of the spitter that fired it.
  - The prefix `YOU ARE HIT by a shot` is kept, and the bots still classify the hits as "shot" (98).
  - QA 104 then showed the south-east line live (`YOU ARE HIT by a shot from the south-east`), consistent with the geometry and the `cue:` line.
  - The player can now say which side a hitting shot came from and connect it to a cue line they saw. The message adds no distance, time or spitter identity, so it does not make the text view easier than the graphical build.
- **Hole B (late swipe explanation) is closed.**
  - W5 passed at 30 and 60 FPS for grub and brute. The line `the <variant>'s lunge had already started, the swipe was too late to stop it` appears before the hit line, and the lunge completes unchanged.
  - W6 showed no spurious line in the wind-up (grub, brute) or recovery cases.
  - The manual now states it too (104 V1 and V2: no stray markers, bullets well formed).
- **The one failure in the round** (98: stray edit marker in the manual) was a text defect. It was fixed and re-verified (104 V1, V2, V3: no markers anywhere). It did not touch gameplay.
- **D-013 item 4 pre-commitment is met.** The wording passed QA (104), the suite is green (69 OK in 98 and 104), and bots were unchanged. 98 shows the bots' hearts and clears inside the combat.md limits at 60 FPS, `bots.py` was unchanged in this round, and the suite includes the bot tests.

### Known gaps weighed and accepted

- **Bots not re-run in 104; no before/after trace baseline (W7).** Nothing in the change could alter behaviour: wording only, a text-reading change, and the suite is green. Accepted.
- **Only the south-east wording was seen live (60 FPS).** The other W1 directions and 30 FPS in the practice room were shown in 98. The remaining direction logic is covered by `ShotSourceTest.test_direction_words_at_both_rates` in the suite. Accepted.
- **W2 at 30 FPS, W3 (other substrings), W4 hurt window, W6 (approach, stagger, kill, 30 FPS brute), W8 partly.** These are the same text paths checked in the shown cases. The messages are computed from a locked shot vector or a phase flag, independent of frame rate. Accepted.
- **R3-8 at 60 FPS, the room 3 pure sidestep, and the 30 FPS cancel and recovery swipe in room 3** were already accepted in D-013 item 5.
- **Visual criteria V1–V11 need a graphical build; V12 is open.** These are outside what a text-view build can show. They move to a proposed Goal.

### Honest limits of this verdict

- All evidence is scripted or QA-traced. No live human has played the new wording.
- "Goal met" therefore means: judged against the success condition on the text-view build, with the cause of every hit and every late swipe now visible. It does not mean a live player has confirmed the build is engaging. That confirmation is a proposed Goal below, not an open clause of G-001.
- Review did not find a trigger for an Owner escalation (D-009 item 4 was not fired in pass 3, and nothing since changes that).

### Decisions whose "revisit when" was checked

- **D-009:** the variant-aware playtest was run (88). No melee-sameness trigger. A graphical build does not exist yet, so no re-judgment is due.
- **D-011:** "a human still reports late swipes as unfair" cannot be judged without a live player. Not reached.
- **D-013:** QA's one failure was handled in one round (as D-013 item 4 allows). "A human still cannot tell what hit them" has no evidence. Not reached.
- None is reopened.

## Next issues (proposed Goals, not extensions of G-001)

1. **Visual readability on a graphical build.** Visual criteria V1–V12, hit-source and late-swipe readability judged by sight. This is the real test of "readable threats" for sighted play and replaces the text messages' role.
2. **Live-player confirmation of the wording.** One live player session on this build (not scripted rules), to see whether the new hit-source and late-swipe lines settle the "what hit me" and "why did my swipe not cancel it" questions. Open this together with Goal 1 or as its first step.
3. **Grub sameness, dodge-heavy spitter rooms, and the room 5 brute tail.** Open each only if a live player reports it. The first lever for the brute is D-004 Option 3; for flat spitter rooms the tuning levers (interval, offset) come first (D-005, D-012).

## Owner items at Close

- The stray last line of D-007 cannot be removed by any step. The Owner needs to delete or confirm it.
- No Owner decision on direction is needed.

## Decisions already made

- D-001: one-button combat. D-004 to D-007, D-009 to D-013: stand.
- New: **D-014** (this step).

## Constraints

- Close per D-013. Do not open another QA round, Diagnose or playtest inside G-001.
- Proposed Goals above are new Goals and must not be folded into G-001's route.

## Open questions

For `studio`:
1. Mark Route row 30 done (goal-met) and row 31 (Next) as Close. Set the Goal outcome with the limits listed in Findings.
2. List the three proposed Goals and the D-007 Owner item at Close.

## Expected output

The Studio Closes G-001 and records the proposed Goals and the Owner item.

## Sender assessment

Confidence is fairly high that the success condition is met on the text-view build. The gap left by pass 3 was narrow and has been closed, and each hole has direct QA evidence at both frame rates. The weakest point is that no live human has seen the wording. I judged this a follow-up Goal, since the success condition asks that the player can tell why, and the text now states the cause for every damaging shot and every late swipe.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#current-state, goals/G-001-combat-monotony/goal.md, design/combat-step94.md, repo/manual.md
- Decisions: decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md, decisions/D-014-review-pass-4-goal-met.md
- Previous handoff: goals/G-001-combat-monotony/105-studio-to-game-director.md
