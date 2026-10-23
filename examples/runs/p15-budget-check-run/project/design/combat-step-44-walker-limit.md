# Combat design note: criterion 13 walker limit (step 44, build 0.6)

Status: amends criterion 13 of `design/combat.md`. Where this note and `combat.md` differ on criterion 13, this note governs. No other criterion, rule or parameter changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-006.

## G-002 applicability annotation

D-019 ends application of this note's old rooms 3–5 aggregate gates to the G-002 boss configuration and continuous run. This includes 13a–d, the old aggregate FPS checks and historical figures in 13e–f, and their aggregate reporting/revisit/re-verification requirements. The historical G-001 ruling and results remain unchanged below.

Independent rooms 1–2 comparisons, independent rooms 3–4 dash rules, shared combat regression and independent-room 3-heart starts remain. Independent rooms 3–4 bot results are reported separately at 30 and 60 FPS. No new aggregate gate is derived from 3–7 or 2/3. The complete replacement and measurement route is `design/final-boss-and-continuous-run.md` §8; it governs G-002 application over this note's historical “unchanged” references to criteria 15–16.

## Question

The walker bot on build 0.6 loses 7 hearts in rooms 3–5 at 60 FPS (4 at 30 FPS). Criterion 13 allowed at most 6. All other criterion 13 limits hold.

## Ruling

7 hearts is not a breach of intent. The limit of 6 was too tight, and it was never derived. Step 22 recorded 6 as "exactly the upper limit" of the 0.5 observation, so it was a snapshot of one bot result.

The purpose of criterion 13 is a gradient: ignoring the aim cue is costly but not hopeless. The 0.6 evidence shows both halves:

- **Costly.** The walker loses 4 (30 FPS) and 7 (60 FPS) hearts. The dodger loses 0 and clears 3/3, and uses 7 or more dashes per room. The camper clears 0 of 3. The gap between ignoring and reading the cue is larger than in 0.5.
- **Not hopeless.** The walker still clears 2 of 3 rooms at both rates. It is not walled out.

Why the hearts ceiling was the wrong tool:

- Each room has 3 hearts. A room the walker clears must have been survived, so it costs at most 2 hearts.
- A walker that clears 2 of 3 rooms therefore loses at most 3 + 2 + 2 = 7 hearts in rooms 3–5. The clear count is what carries "not hopeless". A hearts ceiling below 7 only forbids particular distributions of the same outcome. For example, 3+2+2 at 60 FPS is forbidden, while 3+2+1 is allowed. That says nothing about the gradient.
- The walker decides on a 0.15 s grid. The engineer saw per-room totals move in opposite directions between 0.5 and 0.6. A one-frame difference in a sidestep decides whether a shot hits (criterion 16d). Tuning rooms to move a bot's total by one heart would fit the room to the bot's grid phase, not to any player-visible behavior.

I did not change a room or enemy parameter, for these reasons:

- Both D-004 and D-005 expected this movement. The brute no longer being cancelled raises the walker's losses; consumed shots lower them. The net is what the rules produce.
- Any parameter change would force QA to re-verify criteria 11, 13, 14, 15, 18, 20 and 21 for no player-visible gain.
- D-004 and D-005 stay as they are.

## Amended criterion 13 (replaces the numbers in `combat.md`)

**13. Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate (30 FPS and 60 FPS) separately, in rooms 3–5 summed:

- a. The walker clears at least 2 of the 3 rooms. This is the "not walled out" gate.
- b. The walker loses at least 3 and at most 7 hearts. The lower limit is the "costly" gate. 7 is the largest total consistent with 13a (3 hearts per room, at most 2 lost in a cleared room), so the upper limit is a consistency check and not an independent gate.
- c. The dodger loses at most half of the walker's total and clears 3/3.
- d. The camper clears fewer of rooms 3–5 than the walker.
- e. Per-room walker figures are not criteria. The 30 and 60 FPS totals need not match (16d). The two rates are checked separately and not as a range.
- f. Measured values: 0.6 walker 4 lost / 2 cleared at 30 FPS, 7 lost / 2 cleared at 60 FPS. Dodger 0 lost / 3 cleared at both. Camper 0 cleared at both (engineer's figures; QA re-measures).

Reporting rule: QA reports to `game-designer` any measured value that fails 13a–13d. A walker total anywhere in 3–7 with at least 2 rooms cleared is a pass and needs no report, even if it differs from the figures above.

Criteria 14, 15 and 16 are unchanged. Criterion 16c (dodger agrees between rates) and 16d (walker need not) still apply.

## Which figures would change this ruling

The ruling depends on the gradient, not on the exact engineer figures. These QA results would reopen it:

1. The walker clears fewer than 2 of 3 rooms at either rate. That means walled out, and the response would be a room or enemy parameter change, or Director input if it touches D-004 or D-005.
2. The walker loses fewer than 3 hearts at either rate. That means ignoring the cue is not punished enough. The 30 FPS margin is only 1 heart (4 against 3).
3. The dodger loses more than half the walker's total, or fails to clear 3/3.
4. The camper clears as many rooms as the walker or more.
5. QA finds a difference between rates that comes from a rule and not from bot timing (16e). That is a build defect and not a tuning question.

A QA 60 FPS walker figure of 6 or 7 with 2 rooms cleared changes nothing.

## What QA re-verifies

Only criterion 13 against the amended limits, using `run_bots` on the unchanged 0.6 build at both rates. QA also confirms that the walker's 30/60 FPS differences come from the 0.15 s decision grid (16e). Nothing else needs re-verification, because no rule or parameter changed.

## Experience signal (playtest and Review)

A player who ignores the aim cues in rooms 3–5 is hurt often and may fail a room. They can still finish the three rooms without being locked out, and a player who reads the cues does clearly better. If the hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5, reopen this note and D-004/D-005 tuning values. Do not rely on the bot figure alone.
