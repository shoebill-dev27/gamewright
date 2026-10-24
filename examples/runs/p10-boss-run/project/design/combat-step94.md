# Combat text view: shot-hit source and late-swipe wording (G-001 step 94)

Owner: game-designer. Basis: handoff 93, Review 92, QA 90, playtest 88, D-005, D-007, D-011, D-013. Wording only. No rule, number, timing, cap, cue or input changes. Where this note and `combat.md` differ on these two messages, this note governs.

## Intent

The player can tell why they got hurt. A shot hit says which way the shot came from. A swipe that was too late says so. The build already behaves correctly in both cases; only the text view hides the cause.

## Message A: shot-hit source

**Format.** The damaging-hit message becomes:

`YOU ARE HIT by a shot from the <direction>`

and the existing suffix (` — hearts n/3`) follows unchanged. The prefix `YOU ARE HIT by a shot` is untouched, so reaction rules and `bots.py` that match it keep working.

`<direction>` is one of eight words: `north`, `north-east`, `east`, `south-east`, `south`, `south-west`, `west`, `north-west`. North is the top of the drawn room (smaller y). East is the right (larger x).

**What the direction means.** It is the side the shot came from, relative to the player: the reverse of the shot's travel direction. A shot travelling west was fired from the east, so the message says `from the east`.

**How to compute it.** Take the shot's locked travel vector (vx, vy) at the contact frame, and let (dx, dy) = (-vx, -vy). Let a = |dx| and b = |dy|.
- If min(a, b) / max(a, b) <= 0.4142 (tan 22.5°), the direction is the cardinal word for the larger axis.
- Otherwise it is the diagonal word for the signs of dx and dy.

This depends only on the shot's fixed velocity, so it is identical at 30 and 60 FPS and independent of the hit frame.

**What the engineer must carry.** Nothing new. The shot already has a locked travel direction in order to move. The engineer reads it at the contact frame, before the shot is removed, when building the message. No spitter id, origin, fire time or position needs to be stored.

**Why this reveals nothing new.** The `cue:` line already gives the line's direction, and the `~` line already draws it for 0.6 s before the shot. The message repeats that same locked direction, from the player's side. It gives no distance, no time and no spitter identity, and the graphical build shows the same direction by sight.

**Scope.**
- It applies only to a hit that deals damage.
- A shot absorbed by a dash or the hurt window still shows no message (D-005, unchanged).
- Grub, runner and brute hit messages are unchanged.

## Message B: swipe too late to stop a lunge

**Trigger.** A swipe damages a grub, runner or brute that is in its Lunge phase and does not kill it. Hits in other phases and kills are unchanged.

**Format.** One line, at the moment of the swipe result and before any `YOU ARE HIT by` line of the same frame:

- `the grub's lunge had already started, the swipe was too late to stop it`
- `the runner's lunge had already started, the swipe was too late to stop it`
- `the brute's lunge had already started, the swipe was too late to stop it`

The line uses the variant name, as in D-011. It must not contain `rears back`, `takes aim` or `YOU ARE HIT by`, so no existing reaction rule fires on it. A runner has 1 HP, so a damaging swipe kills it and the runner line appears only if a future HP change allows it. The text is still defined for all three variants.

**Unchanged.**
- The brute's wind-up line `the brute shrugs off the swipe` and its rules (criterion 19).
- The lunge itself. A swipe in the lunge does not cancel, shorten or delay it, and the swipe's 1 damage applies as before.
- A swipe that kills a grub in its lunge shows no new line.

**Why this reveals nothing new.** It states a fact the player could already see: the `cue:` line and `~` lane end when the lunge starts. It gives no prediction.

## Edge cases

- Two shots hit in one frame: only one damages (D-005). One message, with the direction of the shot that dealt the damage.
- Swipe and hit in the same frame: the swipe line comes first, then the hit line.
- Swipes in recovery, approach or stagger: no new line.
- One message per swipe. No batching and no repeat suppression.

## Acceptance criteria (QA, 30 and 60 FPS, `play.py --view player`)

Practice room (`room empty`, `spawn`, `player`), all at both rates.

- **W1. Direction words.** A still player at (8,4) is hit by a single spitter's shot. Check these placements:
  - spitter at (15,4): `from the east`;
  - spitter at (8,0): `from the north`;
  - spitter at (1,4): `from the west`;
  - spitter at (8,8): `from the south`;
  - spitter at (15,0): `from the north-east` (ratio 4/7 = 0.57 > 0.4142);
  - spitter at (15,7): `from the south-east` (shot travel vector about (-0.92,-0.39); reversed (0.92,0.39); ratio 3/7 = 0.43, which is above 0.4142, so the diagonal applies; QA checks the traced value against this).
  
  In every case the full line begins `YOU ARE HIT by a shot from the `.
- **W2. Real room.** In room 4 and room 5 a damaging shot hit shows a direction word consistent with the `cue:` line direction of the spitter that fired it (the reverse of the cue direction).
- **W3. Prefix kept.** `text "YOU ARE HIT by"` and `text "by a shot"` match, and `rears back` and `takes aim` still match their lines. A reaction-rule script using each of the three substrings behaves as before the change.
- **W4. Absorbed shots.** A shot absorbed by a dash or the hurt window produces no hit message, as before.
- **W5. Late swipe.** A standard grub at (10,4), player at (8,4) facing it, one swipe timed from the trace during the lunge (0.3 s long, after the 0.5 s wind-up; for the brute, after its 0.7 s wind-up) so it lands on the grub in reach. The player view shows `the grub's lunge had already started, the swipe was too late to stop it`, and it appears before `YOU ARE HIT by a grub`. The grub loses 1 HP and still finishes the lunge. Repeat once with a brute and the `brute` wording.
- **W6. No line elsewhere.** The late-swipe line does not appear for a swipe in wind-up (the grub is cancelled; the brute shows `shrugs off`), in recovery, in approach or in stagger, and not for a kill.
- **W7. No behavior change.** Compared with the build before the change, with the same scripts at the same rate: hit times, hearts, cue times, shot fire and contact times, lunge and recovery times and the in-flight counts are identical to ±1 frame. Criteria 1–21 of `combat.md` hold. `bots.py` runs unchanged with the suite green, and the bots' hearts and clears are as before.
- **W8. Frame-rate independence.** W1 to W6 give the same wording at 30 and 60 FPS.

## Experience signals (Review and playtest, not for the Playtester's handoff)

- A player can say which side a hitting shot came from, and can connect it to a cue line they saw.
- A player who swiped a lunging grub and was hit can say "I was too late", and does not ask what makes a swipe cancel.

## Rejected alternatives

- Naming the spitter by coordinates or an ordinal: needs the shot to carry an origin, and adds identity the cue lines never showed. Not chosen.
- Showing distance or fire time in the hit message: gives the text view more than the graphical build gives. Not chosen.
- Keeping the shot visible after contact: touches D-005. Not chosen.
- A line for every swipe that does not cancel: noise, and it explains nothing in the other phases. Not chosen.
- No Decision record: none of these alternatives constrains later work beyond this note.

## Changed documents

- New: this note.
- `design/combat.md`: pointer added at the top (done, the "Step 94" paragraph).
- **`repo/manual.md` could not be edited (not in my write paths).** The text to apply is given below.

### Manual wording (for the Build step)

Replace the sentence "Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot`." with:

"Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot)."

After "A swipe that lands after the lunge has begun does not cancel it." add:

"When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute)."
