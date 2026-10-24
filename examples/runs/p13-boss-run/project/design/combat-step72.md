# Combat design note, step 72: room 3 gets a second ask (a standard grub) and a tighter spitter layout

Status: room content only (room 3 table row). No rule, parameter, cap, cue, timing or input change. Where this note and `design/combat.md` differ on the room 3 row, criterion 12 or the room 3 purpose, this note governs. Fold into `combat.md` the next time it is edited. Decision: D-012. D-001, D-004 to D-007 and D-011 are untouched.

## Intent

Room 3 still teaches the aim cue first, with the verified schedule (first shots 1.8, 2.6, 3.4 s). After that it asks a second, different question: a lunge lane on top of aim lines. The player must move toward and through the room instead of repeating "aim, dash, shot lands behind me". The last spitter is never far from the others, and a hunting grub keeps the player moving, so the room does not become a long standoff against one spitter in a far corner.

## Diagnosis (design terms)

1. One ask. Room 3 has only the aim-line ask, answered the same way each time (sidestep or dash). With nothing else to answer, attention drops after the third or fourth repeat (playtests 53 and 63).
2. A standoff has no pressure to end it. Spitters are stationary, HP 2, and fire every 2.4 s. A player who kills two and leaves the third far away loses nothing by dodging for a long time. The east spitter at (14,7) is 12 tiles from the west spitter at (2,7), so reaching it is a long walk. Shots take about 4 s to cross, so each dodge is slow and the whole thing reads as a wait.
3. Rooms 4–5 held attention because several different asks overlap. Room 3 is the only room with a single ask.

## Options considered

| Option | Second ask | Pressure on a lone spitter | Touches cap or cue rule? | Verdict |
|---|---|---|---|---|
| A. Add one standard grub, far from the player's start, and move the third spitter closer | Lunge lane (step aside or dash) | The grub hunts the player, so staying still costs hearts. The spitters are closer together. | No | **Chosen** |
| B. Add one runner instead | Fast short lane (0.35 s warning) | Same | No | Rejected: the 0.35 s warning on top of 0.6 s aim cues in the teaching room is a harsh jump. Rooms 2 and 4 already cover the runner. |
| C. Add a brute | "Step aside, then punish" | Strong | No | Rejected: HP 4 and a 1.2 s recovery add a long fight to a room that is meant to teach. The brute stays in rooms 2 and 5. |
| D. Replace one spitter with a grub (two spitters plus grub) | Same as A | Strong | Yes. It changes the 1.8/2.6/3.4 s schedule and the in-flight bound. | Rejected: breaks criterion 11a and forces the D-007 verification to be redone. |
| E. Gap rule 0.2 s in room 3 (D-007 prepared fallback) | None | None | Yes | Rejected: fixes a different problem and changes a verified room. |
| F. New mechanics (reinforcements arriving later, a spitter that speeds up when alone, healing) | n/a | n/a | n/a | Outside this step: a new system or new enemy behavior. Not specified. |

## Chosen option: A

### Room 3 contents (replaces the room 3 row)

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 3 | Spitters at (2,1), (10,6), (2,7), in that room-table order (k = 0, 1, 2). Standard grub at (15,0). | 0.8 s / none (unchanged) | Learn the aim cue first, then answer an aim line and a lunge lane together |

Changes against the old row:
- The second spitter moves from (14,7) to (10,6). The order of the spitter list is the same, so k = 0, 1, 2 and the first-shot times are unchanged.
- One standard grub is added at (15,0), in the far corner away from the spitters and from the usual start.

All other room 3 parameters are unchanged: spitter interval 2.4 s, offset 0.8 s, cap 3, no gap rule, the D-007 bound (up to 2 plus the living spitters, so at most 5), and the grub parameters of the standard variant (HP 2, walk 1.0, wind-up 0.5 s, lunge 8.0 for 0.3 s, recovery 0.8 s, swipe cancels wind-up).

### Why these choices

- **Standard grub, not runner or brute.** Its answer is "either" (sidestep, dash or cancel). It is the gentlest lunge, so it is the right second ask for a room that is still teaching. It does not need new text; D-011 names it `a grub rears back`.
- **The grub walks at 1.0 tile/s from the far corner.** The distance gives the delay with no new system: it should not reach 2.0 tiles of the player, and so not start its first wind-up, until well after the third spitter's first cue. Criterion R3-3 checks this and tells QA what to do if the geometry says otherwise.
- **Spitter (10,6).** The largest distance between any two spitters becomes 9.4 tiles (between (2,1) and (10,6)), against 12.4 before. A player at 4 tiles/s covers that in about 2.4 s, or sooner with a dash. Spitter position affects only where the shot starts, not any cue time.
- **The grub pressures a stationary or kiting player.** A player who stands off and dodges shots is hunted by the grub, which asks for a lane answer or a kill. The room does not end until the grub is dead too, and it is a 2 HP target that can be swiped in recovery.
- **The one-at-a-time rule is untouched.** It applies among grubs. With one grub it changes nothing in room 3. Spitters are not gated by the grub and the grub is not gated by spitters.

### Edge cases

- **Grub wind-up while a spitter cue is running (or the reverse).** Allowed. They are two separate cues: a thin line and a 1.2-tile lane. A dash clears both. A sidestep must clear both. Readable threats holds because each cue is visible for its full duration. This is the same overlap that rooms 4–5 already have, except there the gap rule spaces the spitter cues from each other, which does not matter for a grub.
- **Cap and in-flight bound.** The grub does not count as a shot and does not delay a cue. D-007 stands: shots in flight never exceed 2 plus the living spitters.
- **Blocked contact (D-005).** Unchanged. A lunge that touches a protected player is spent. A shot that touches a protected player is consumed.
- **Grub killed early.** Room 3 continues with the spitters only. The standoff risk then returns for the last spitter, but the layout keeps it close (see R3-8).
- **All spitters killed first.** The grub fights as a single standard grub, as in room 1.
- **Player dies or room cleared.** Existing handling.
- **Player start position.** I could not check the start position in this packet. R3-3 is written so QA measures it from a trace.

## Acceptance criteria

### Verifiable (QA, `play` and `bots`; every check at both 30 and 60 FPS)

- **R3-1. Contents.** Room 3 contains exactly three spitters at (2,1), (10,6), (2,7) and one standard grub at (15,0). Room 3 contains no other enemy. Rooms 1, 2, 4, 5 are unchanged (criterion 12).
- **R3-2. Teaching schedule intact.** With a still player, the first spitter shots are at 1.8, 2.6 and 3.4 s ±1 frame, each cue 0.6 s ±1 frame before its shot (criteria 9, 11a). The grub changes none of these.
- **R3-3. The grub comes after the lessons.** With a player standing still at the room's start position, the grub's first wind-up message (`a grub rears back`) appears no earlier than 4.0 s after the room starts. Expected from geometry: the grub has to cover several tiles at 1.0 tile/s before it is within 2.0 tiles (derived, not measured). If QA's trace shows an earlier start, QA reports the measured time and the start position to `game-designer`, who moves the grub (tuning, no new spec step).
- **R3-4. The grub obeys the existing grub criteria in room 3.** The cue is at least 0.5 s before the hit (1); a 1-tile sidestep within 0.4 s of the cue avoids it (2); a dash from the cue until 0.1 s before the lunge ends avoids it and the player takes no damage after the dash (3, 21); a swipe in reach during the wind-up cancels it (6); two swipes kill it (6, 8); the recovery is safe (5).
- **R3-5. Spitter criteria hold with the grub alive.** Criteria 9 and 10 (cue and dodge) and 17 hold for shots fired in room 3.
- **R3-6. The D-007 bound is unchanged.** Criterion 11 as amended (step 46 note a–e) holds: the derived count of shots in flight in room 3 is 3 to 5 after a cap delay, and above 5 is a defect. No cue start is delayed or advanced by the grub: cue start times with the grub are equal to the times without it, ±1 frame, for the same still-player script until the grub's first lunge.
- **R3-7. Room end.** Room 3 is cleared only when the three spitters and the grub are all defeated. Killing the last spitter with the grub alive does not clear the room, and the reverse.
- **R3-8. The last spitter is close.** The distance between any two spitters in room 3 is at most 9.5 tiles. In a scripted run that kills the grub and two spitters, a player that then walks straight to the last spitter (dashing when a cue is on) and swipes it clears the room within 6 s of the previous kill (derived: about 2.4 s of walking plus two swipes, so about 3 s). This checks that the layout allows a quick finish. It does not force the player to take it.
- **R3-9. Messages.** The grub's wind-up and hit use whatever messages the build has (`a grub rears back`, `YOU ARE HIT by a grub`), whether or not Build 22a (D-011) is in. A rule `text "rears back"` reacts to it.
- **R3-10. Frame-rate independence (16).** Criteria 1–12 and 17–21 hold at both rates in room 3. No new tolerance is introduced.

Bots (criteria 13–15): the walker faces one more lunge in room 3, so the sum of its hearts lost in rooms 3–5 is expected to rise. At 60 FPS it was already at the upper limit of 6 (criterion 13). The limit may be exceeded, and the clear count may fall below 2. The dodger should be unaffected or have slightly more use for the dash. These are **expected effects, not verified**. QA measures them on the Build and reports values outside the limits to `game-designer` as a tuning question, not a build defect, as in steps 22, 35 and 38. If the bots key on room 3 contents, the Build updates them (test tooling).

### Experience signals (playtest and Review, not for the Playtester's handoff)

- In room 3 the player describes two kinds of threat: "the lines from the spitters" and "the grub that comes for me", and answers each differently.
- The first minute of room 3 is still described as learning the aim line, with the grub appearing as a new thing after that, not as a surprise during the first cues.
- The room is not described as "the same thing again" for most of its length, and no stretch of about 10 s consists of dodging one far-off spitter.
- A player who hears or sees a lunge cue during a shot cue can say which one to answer first, or that one move answered both.
- Nobody reports a shot or lunge that "came out of nowhere".

## Changed design documents

This note (new). `combat.md` is not edited here. The room 3 row, criterion 12 and the room 3 purpose line are governed by this note until folded in. D-012 records the choice.

## Open questions

1. The player start position in room 3 was not available to me. R3-3 is the guard; QA reports the measured grub arrival time.
2. Whether a human still produces a long single-spitter standoff cannot be known from scripts. A live or hand-timed playtest of room 3 is the check (D-010 item 5). If a standoff persists, the next levers are a runner in place of the standard grub (Option B) or a second grub, then a larger room change. A new enemy or new behavior would go to `game-director`.
3. Whether the grub on top of aim cues is too much for a room that teaches. If the playtest says so, move the grub later (further away) before changing anything else.
