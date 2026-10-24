---
kind: handoff
goal: G-001
seq: 35
from: game-designer
to: studio
stage: Route
outcome: done
---
# 35: game-designer → studio — Design spec for Options 1 and 2 (cue gap in rooms 4–5, brute not cancelled), Option 3 deferred, manual wording given

## Task

Route to **Build** (build 0.6, `gameplay-engineer`), then QA at 30 and 60 FPS, then a hand-timed Playtest. The spec is in `design/combat.md` (marked "step 35"), the decision in `decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md`. No Decide step is needed: no new enemy, no healing, no new input, no scope change. The visual spec was not changed (items for `art-director` below).

## Context

G-001 (combat monotony). Handoff 33 asked for a spec for Options 1 and 2 of handoff 31, a ruling on Option 3, and exact manual wording. The parallel QA trace of spitter fire times in rooms 3–4 (handoff 34) was not available. The spec for Option 1 does not depend on it. I ran no `play` or `bots` this step, because the changes are to a build that does not exist yet. So I verified nothing about build behavior. The bot expectations below are derivations and are marked.

## Findings

### Rulings

1. **Option 1: a cue gap rule in rooms 4 and 5.**
   - Rule: a spitter in those rooms may start a cue only if (a) no other spitter in the room has a cue running, (b) the last shot in the room was at least 0.6 s ago (1 ms tolerance so an exact tie counts), and (c) the existing shot cap allows it. Otherwise it waits 0.2 s and checks again (the existing cap-delay mechanism, and the delay carries forward).
   - Parameter: first-shot offset 1.2 s in rooms 4–5 (first shots at 1.8 s and 3.0 s, then alternating every 1.2 s, each spitter every 2.4 s). This meets the rule exactly, so the rule normally delays nothing. Room 3 and practice rooms keep offset 0.8 s and no gap rule, so **criterion 11 for room 3 does not change**.
   - It does not depend on the "in sync" claim. If two spitters ever would fire together, the second waits and the pattern settles to alternating.
   - Cap stays 3. Interval stays 2.4 s. Run length is unaffected.
   - Consequence I want the Build step to know: with 1.2 s spacing and shots living up to 5 s, the cap (fewer than 3 in flight at a cue start) can delay a cue when the player is far from the spitters. That is accepted.
2. **Option 2: the brute's wind-up is not cancelled by a swipe.**
   - A per-variant flag "swipe cancels wind-up": standard yes, runner yes, brute no. A swipe that damages a winding-up brute deals 1 damage, shows the message `the brute shrugs off the swipe`, does not stagger it, does not remove its cue, and the lunge goes ahead on its normal timer. A swipe that kills it in wind-up kills it with no lunge and no message. The dash still avoids the lunge.
   - Derivation: the brute's recovery is 1.2 s and a swipe takes 0.35 s, so up to four swipes fit in one window if the player is in reach and facing from the first frame, about three with a human reaction. So a full-health brute normally needs two windows ("dodge, hit, dodge, hit"). Not measured.
3. **Option 3 (spitter in room 2): deferred.** Reasons: it changes criterion 14 and the identity of room 2 in the same slice as the brute rule, which both address the "dodge the brute forever" problem. If both are built, the playtest cannot say which one worked. Revisit after the playtest (D-004). Rooms are unchanged in this slice.
4. **Signal beyond the manual (Option 2): yes, one.** The in-game message `the brute shrugs off the swipe` (a rule in the spec, text view). For `art-director` (presentation): a hit reaction on a brute swiped in wind-up that reads as "took the hit, not interrupted", clearly different from the stagger of a cancelled grub (V10 and V8 stay valid). I kept the existing `a grub rears back` message for all variants unchanged, so reaction rules with `text "rears back"` keep working. A brute-specific rear-back message was not asked for.
5. **Visual spec:** no change made. One sentence is outdated for rooms 4–5 ("spitter cues are normally 0.8 s apart ... rarely overlap"): there they are at least 0.6 s apart and never overlap by rule. `art-director` can update that.

### Changed and new criteria (all in `design/combat.md`)

| Criterion | Change |
|---|---|
| 6 Cancel | Now standard grub and runner only. A kill in wind-up still has no stagger and no lunge, for every variant. The brute is criterion 19. |
| 8 Variants | Brute still dies to four swipes in any phase (clarified). |
| 3 Dash works | Stated to hold for the brute too (the brute's answer now). |
| 11 Stagger and cap | Room 3 unchanged. Rooms 4–5: first shots at 1.8 and 3.0 s ±1 frame. Never more than 3 in flight in rooms 1–5, must be re-verified in 4–5 (timing changed). |
| **18 (new)** Cue gap in rooms 4–5 | Traces of rooms 4 and 5 (at least 15 s, both rates): no cue overlaps another; every cue starts at least 0.6 s (minus 1 frame) after the previous shot in the room; also after one spitter is killed and under cap delay; cue 0.6 s ±1 frame before the shot. Optional d: if the Build step can force both spitters to the same first shot, the gap must still hold; if not, QA says it was not run. |
| **19 (new)** Brute not cancelled | Practice room, brute about 1 tile away, player in the lane not dashing: (a) one swipe in wind-up: 1 damage, message, no stagger, lunge at 0.7 s ±1 frame, 1 heart lost; (b) two swipes: both deal damage, one lunge; (c) a killing swipe in wind-up: dies, no lunge, no message; (d) dash plus swipe: no damage taken, swipe damage applied; (e) recovery swipe: 1 damage, phase unchanged; (f) standard grub and runner still cancel. |
| 16a | Now lists 18 and 19 among the criteria that hold at both rates; 16e likewise. |
| 13, 14, 15 | Numbers unchanged. Expected effects below. |

### Bot expectations re-derived (none verified; the bots must be run on 0.6)

- **13 (rooms 3–5, walker 3–6 hearts, clears at least 2 of 3; dodger at most half of the walker's total and clears 3/3).** Room 5 has a brute: the walker ignores cues and swipes, so it now takes the lunge it used to cancel. Expect more hearts lost in room 5. In 0.5 the 60 FPS walker was already at exactly 6, so expect the upper limit to be exceeded at 60 FPS and the clears possibly to fall below 2. The effect of the cue gap on the walker could go either way (fire rate is unchanged: one shot per 1.2 s). Rule already in force (step 22): a walker outside the limit is reported to `game-designer` as a tuning question, not a build defect. **Cannot verify without running the bots.**
- **14 (rooms 1–2: walker at least 1 lost; dodger at most 1 lost, clears both).** Walker: the lower limit is safe. Dodger: **at risk** if its policy swipes the brute in wind-up to cancel. Bot rule I set: against the brute (`G`) the dodger sidesteps or dashes on the cue and swipes only in recovery. I could not check what `bots.py` does. **Build step: check the dodger's brute handling and change it if needed** (test tooling). QA reports dodger hearts in rooms 1–2 at both rates.
- **15 (dodger dashes at least once in each of rooms 3–5).** At risk in room 4: with a 0.6 s gap the dodger may sidestep everything and never dash. If it fails, QA reports to `game-designer`; it is not a build defect and I do not want the gap shortened to force it. **Cannot verify without running the bots.**
- **16c (dodger agrees between rates, per-room hearts within 1, same cleared set):** no reason for a change; verify.

### Exact manual wording (`repo/manual.md`, applied by the Build step)

Change the title to the new build number (for example `# Lantern Depths — how to play build 0.6`).

1. In "On screen", replace the Grub line with:

   `- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow, 4 swipes, long warning; a swipe does not interrupt it.`

2. In "Warnings", in the first bullet ("A grub rears back"), replace the sentence from `The line is fixed ...` to `... to cancel the lunge.` with these two sentences:

   `The line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the lunge. A swipe (within 1.5 tiles) that lands during the warning cancels the lunge of a grub or a runner; once the lunge has started, a swipe no longer stops it.`

3. In the same bullet, after the sentence `After a lunge the grub is harmless for a while: that is the time to swipe it.` and before `Only one grub rears back or lunges at a time.`, add:

   `A brute is different: a swipe during its warning hurts it but does not stop it ("the brute shrugs off the swipe"), and it lunges anyway. Step aside or dash, then swipe it while it recovers (1.2 s).`

4. In "Warnings", the spitter bullet: replace `Shots are slow-looking but travel 3 tiles a second, and no more than 3 are in the air at once.` with:

   `Shots are slow-looking but travel 3 tiles a second. In rooms 1–5 no more than 3 are in the air at once. In rooms 4 and 5 the spitters take turns: after one takes aim and spits, there are at least 0.6 s before another takes aim.`

5. In "Warnings", the last bullet: replace `A swipe that interrupts a grub's warning staggers it for 0.4 s.` with:

   `A swipe that interrupts a grub's or runner's warning staggers it for 0.4 s. A brute is not staggered.`

(Scope of "3 in the air": rooms 1–5 only; a practice room with four or more spitters can have more, as the spec says.) The swipe-only-during-warning item from QA (handoff 32) is covered by item 2. It is a wording fix and not a rule change.

### What QA must verify

- Criteria 18 and 19 as written, at 30 and 60 FPS, and criteria 1–12, 17 re-run for regressions (6, 8, 11 are changed). Especially: room 3 timing unchanged (1.8, 2.6, 3.4 s); rooms 4–5 first shots at 1.8 and 3.0 s; at most 3 in flight in rooms 1–5.
- Standard grub and runner cancel and stagger exactly as before (19f).
- The bots on 0.6 at both rates: report the numbers for 13, 14, 15, 16c, and compare with the 0.5 values given in `design/combat.md`. Anything outside the criteria goes to `game-designer` with the numbers, and not "fixed" in the build. Say clearly what was not run (for example the forced-sync test in 18d).
- Manual lines applied as given, and the version title updated.
- The result of handoff 34 (spitter fire times in rooms 3–4 in build 0.5) when it arrives: if it shows the spitters really did fire together in 0.5, tell me. The gap rule covers it either way, but the cause would then be a build or cap-delay defect in 0.5.

### What the Playtester should focus on (without the expected result)

Hand-timed, no script reactions at a fixed delay. Rooms 2, 4 and 5, at least two attempts each. In every room: what you did against each kind of enemy and why; what you thought was going to happen before each hit and what happened instead; for each hit taken, what hit you and what you could have done. Rooms 4–5: when you got hit by a shot, whether the shot came from a line you had seen being drawn, and what you were doing at the time. Room 2: what you did about the large enemy, and whether you finished the room. Note anything you tried to do with the attack button on any enemy that did not behave as you expected. Report whether you used the dash, when, and why. Do not tell the Playtester about the cue gap, the brute flag or the messages.

## Decisions already made

- D-001 (attack and dash only): kept. D-002, D-003 (contact sampling, graze, exactly the reach): untouched.
- D-004 (new, this step): the cue gap rule and offset in rooms 4–5, the brute flag, Option 3 deferred. Alternatives rejected there: offset only without a rule, cap 2 in rooms 4–5, the rule in room 3, a new melee enemy or a wider lane, a partial-cancel brute rule, and Option 3 in this slice.

## Constraints

- No new input, no new enemy type, no healing, no scope change. Correct at 30 and 60 FPS (all timings run on accumulated time). Lane geometry is identical for all variants. The build must not change contact sampling.

## Open questions

- For `game-director` / Studio: none that need a Decide step.
- Whether a human who has not read the manual notices the brute's "shrug" message (the only in-game signal). If the playtest shows it is missed, the next step is a presentation change for `art-director`.
- Whether the walker/dodger numbers for 13–15 hold on 0.6: only the bots can say.
- Whether Option 3 or a room change is needed: decide after the hand-timed playtest.

## Expected output

Studio routes: Build (`gameplay-engineer`: spec items 1 and 2, the manual lines, check/adjust the dodger's brute policy, provide a forced-sync test if cheap), QA (above), then the Playtester briefed as above, and `art-director` informed of the two presentation items (brute hit reaction; spitter-cue spacing remark). A Build is needed.

## Sender assessment

Confidence: high that the rules are complete and testable (every new rule has a number and a player-observable check). Medium that the Option 1 offset and gap will feel right to a human (derived from the spec: a 0.6 s gap is enough for a 1-tile sidestep, which takes about 0.15 s plus reaction, but not measured). Medium-low on bot expectations for 13–15: the brute change plausibly pushes the walker over its limit in room 5 and the dodger's brute handling is unknown to me. I ran nothing, so nothing here is verified against a build.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/33-studio-to-game-designer.md
