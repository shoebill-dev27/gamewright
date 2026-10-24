---
kind: handoff
goal: G-001
seq: 92
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 92: game-director → studio — Review pass 3: goal not met by one clause only ("the player can tell why" for shot hits and late swipes). No Owner escalation. One wording-only Design step, then Build and Verify, then a paper Review that is expected to close the Goal.

## Task

Route the Review result. The verdict is **goal-not-met**, with fairly high confidence that the gap is small and bounded. D-013 records it.

## Context

Goal G-001. The success condition has two halves: different situations call for noticeably different play, and the player can tell why. The inputs are playtest 88 (scripted, reaction rules, not live), QA 76, 82, 86 and 90, and the earlier playtests 27, 53 and 63. I ran no `play` or `bots`.

## Findings

### Half 1: different situations, different play. Met.

- **The melee asks three different things** (63, 88, earlier passes).
  - The runner is "act early; the warning is 0.35 s".
  - The standard grub is "either".
  - The brute is "step aside, then punish; a swipe does not stop it". Playtest 88 again called the runner and the brute distinct.
- **Spitters ask something else again.** The answer is to cross or dash the aim line, or close in.
- **Rooms 4–5 hold attention.** Playtest 88 called room 4 "the most tense". Playtests 27, 53 and 63 agree. Several asks overlap there, and that is where the variety comes from.
- **Room 3 now has a second ask** (D-012). Playtest 88 reports no long single-spitter standoff there. It cleared room 3 in 10.9 s and described two kinds of threat. It still called the stretch around 4.5–6.5 s "busy but passive". I treat that as tuning-level, not a gap against the Goal.
- **D-009 escalation condition: not fired.** The question is whether the melee still reads as one fight. It does not: runner, grub and brute were told apart again in 88, and the brute is not merely kited. The room 5 brute tail was a standoff, but the tester attributes part of it to a rule that only attacked within 1.5 tiles. It is one scripted observation and is not the D-004 trigger. No Owner question exists.

### Half 2: the player can tell why. Mostly met, with two confirmed holes.

- Hits from grubs, runners and brutes were nearly always traceable to a visible cue (88). The D-011 variant names worked: nobody was confused about which enemy hit them.
- **Hole A (shot hit has no source).** In room 4 the tester could not tell which shot hit them in two of three hits. QA 90 confirmed the cause. `YOU ARE HIT by a shot` names no source, and the shot is consumed at contact, so no later frame can show it. QA found the dash and invulnerability behaviour correct and could not reproduce the tester's three hits, because the script was lost. This is a readability failure, not a build defect, and it falls under "readable threats" and "the player can tell why".
- **Hole B (late swipe, no explanation).** A swipe that lands after the lunge has begun does not cancel it. That is the correct design, and QA 90 reproduced it at 30 FPS. No player-view line says the lunge had already started. Only the brute has a "shrugs off" line. The tester raised it in three places (rooms 2, 3 and 5) and asked directly, "What exactly makes a swipe cancel a rear-back?"

These two are the same kind of fault. The build is right and the text view does not show the cause. D-011 already treated this class of fault as in scope ("the player can tell why"). A third Diagnose is not needed: the cause is known and the fix is wording.

### Remaining observations: not blocking the Goal

- **Grub sameness (88 issue 1).** The tester was dashing every grub in room 1, a pure teaching room. Room 1 is meant to teach one cue. Grubs differ across rooms by context (runner and brute in room 2, spitters in rooms 3–4). Playtest 88 itself calls the other rooms' grub handling medium impact, and the tester's own rules (dash on every rear-back) forced the sameness. Not acted on. Candidate for a later Goal.
- **Dodge-heavy spitter rooms (88 issue 4).** This is inherent to the spitter's role and is partly what makes rooms 4–5 tense. Not acted on. If a live player reports it as flat, tuning levers (interval, offset) come first, per D-005 and D-012.
- **Brute tail in room 5 (88 issue 5).** Not confirmed outside the tester's rule limits. D-004 Option 3 stays deferred.

### Known gaps accepted

- R3-8 at 60 FPS (passes at 30 FPS, 2.37 s against 6 s; geometry fine at both rates).
- The pure 1-tile sidestep in room 3 (passes in the practice room at both rates).
- The 30 FPS cancel and the recovery swipe in room 3 (the cancel was seen at 30 FPS in 76; the recovery swipe is covered at 60 FPS in 86).

I accept all three as known gaps. QA has made its last bounded try. The practice-room evidence covers the same rule, and room 3's change was content only (D-012). No further QA round is planned for them.

**Loop limit.** Diagnose stays barred; no new cause exists. A Design step on wording is not a Diagnose.

### Confidence and limits

All play is scripted, so "tense", "varied" and "passive" are the tester's reading of printed frames. I weighed the tester's admission that the room 5 tail and the room 1 sameness came partly from their own rules, as in passes 1 and 2. The hit-source hole is confirmed by QA, not only by the tester.

## Next issues

1. **Design, wording only, under "readable threats" (inside G-001).**
   - **(A)** Make a shot hit traceable in the text view. For example, name the spitter or its side, or the compass direction the shot came from, in the hit message. It must keep the `YOU ARE HIT by a shot` prefix so reaction rules keep matching. It must reveal nothing the `cue:` and `~` lines did not already show. It must not make the text view easier than the graphical build is meant to be.
   - **(B)** Add a player-view line when a swipe damages a grub that is already in its lunge, saying the lunge had started and the swipe was too late to stop it. Keep the existing brute "shrugs off" line and the existing `rears back` substring.
   - **Limits.** No rule, number, timing or input change. No change to the shot cap, cue schedule or blocked-contact behaviour (D-005, D-007).
2. **Build** the specified wording, then **Verify (QA)** at 30 and 60 FPS. QA checks:
   - the new text appears;
   - existing reaction rules and `bots.py` still work (bots unchanged, suite green);
   - no timing, hit or cue changed.
   This is a text-only check, and no new playtest or room 3 timed run is required.
3. **Review pass 4 is a paper check of QA's result.** I expect to declare goal-met if A and B pass QA (D-013).
4. **Proposed Goals at Close (not extensions of G-001):**
   - visual criteria V1–V11 on a graphical build, with V12 open;
   - grub sameness and dodge-heavy spitter rooms, only if a live player reports them;
   - the brute tail, with D-004 Option 3 as the first lever, only if confirmed.
5. **Owner items at Close:** the stray last line of D-007 that no step could remove.

## Decisions already made

- D-001, and D-002 to D-007, D-009 to D-012: all stand.
- D-009 item 4 (Owner escalation): checked, not triggered.
- New: **D-013** (this step).

## Constraints

- No new input, no change to run length, no new biomes or unrelated content.
- Reuse the existing message system.
- The change must be identical in effect at 30 and 60 FPS.
- Keep the substrings `takes aim`, `rears back` and `YOU ARE HIT by` so existing scripts keep working.

## Open questions

For `studio`:
1. Route Design (wording A and B) to `game-designer`, then Build, then Verify, then Review pass 4 (paper). Mark row 11 (Owner escalation) as not needed.
2. At Close, list the proposed Goals and Owner items in section 4 and 5 above.

## Expected output

The Studio routes Design (A and B) to `game-designer`. No Owner escalation is drafted.

## Sender assessment

Verdict confidence is fairly high on "narrow, one clause". The call between goal-met and goal-not-met was close. The two holes are in the success condition's own words and QA confirmed one of them (A) from a different script than the tester's. A fix is cheap, and the Goal's variety half has been met since pass 2. I chose not to close on a known, confirmed clarity failure, and I bounded the remaining work so Review does not loop again.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, goals/G-001-combat-monotony/goal.md
- Decisions: decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/91-studio-to-game-director.md
