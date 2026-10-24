# Combat design addendum, step 59 (wording of late swipes; cue message per variant)

Status: wording only for point 1 (no rule or parameter change, no build change). Point 2 is a proposed player-facing change, not built, see D-008. Where this file and `design/combat.md` differ, this file governs for the two points below. `combat.md` itself is unchanged in step 59 because its rules already say what the manual must say.

## Intent

A text-view player can tell, from what is printed, (a) when a swipe can still cancel a lunge and (b) which kind of grub is about to lunge. No new information that makes threats harder to read, and no dependence on graphics.

## Point 1: swipe timing wording (no rule change)

Rules already in `combat.md` (unchanged):
- A swipe that damages a standard grub or runner in wind-up cancels it. Stagger 0.4 s. One non-lethal swipe is enough, even on a 2 HP grub.
- A swipe during the lunge, recovery or stagger changes no phase. A lunge that reaches a hurtable player in its path still deals 1 damage.
- The brute is never cancelled by a swipe (D-004).
- Swipe reach 1.5 tiles. A grub starts its wind-up when the player is within 2.0 tiles, so at the start of a wind-up the target may be 1.5–2.0 tiles away and out of reach. A swipe cancels only if the grub is within 1.5 tiles at the moment the swipe lands, which the player can reach by stepping in during the warning (4 tiles/s).

Conclusion: wording is enough. Playtest 53 and QA 56 show both "unfair" swipes landed 0.10 s after the lunge began with the grub out of reach during the whole warning. A swipe-timing rule change (a grace period after the lunge starts, or a larger reach) would make the lunge cancellable after its warning and weaken "step aside or dash" as the answer, and the evidence does not show a rule problem. No rule change is proposed.

Manual wording (exact text, for `repo/manual.md`) is in handoff 59.

Acceptance (verification): the manual says all of: swipe cancels only during the warning; a grub starts rearing back about 2 tiles away, beyond the 1.5-tile reach, so step in to within 1.5 tiles during the warning; a swipe landing after the lunge has begun does not cancel it; one swipe is enough to cancel a grub or runner; the brute is never cancelled.

Experience signal (playtest and Review): a player who swipes a rearing grub from too far, or too late, and is hit can say why ("it was already lunging" or "it was too far") without calling the hit unexplained.

## Point 2: cue message per variant (proposed build change, see D-008)

Proposed text-view start-of-warning messages:

| Variant | Mark | Message |
|---|---|---|
| Standard grub | `g` | `a grub rears back` (unchanged) |
| Runner grub | `r` | `a runner rears back` |
| Brute grub | `G` | `a brute rears back` |

Rules:
- All three contain the words `rears back`, so existing reaction rules `text "rears back"` still match all variants. A rule `text "a grub rears back"` matches only the standard grub after the change.
- Only the message text changes. Timing, the `~` line, the `cue:` line, one-at-a-time, cancel flags and every parameter stay the same.
- No distance, hit points or timing are added to the message. The `cue:` line stays the place for those.
- The message is a text-build presentation. The graphical build keeps its silhouette, size and cadence (visual spec) and is unaffected.
- The spitter and brute-swipe messages are unchanged.

Acceptance criteria (verification, for QA if built), at 30 and 60 FPS, practice room:
- V-a. A runner's wind-up prints `a runner rears back`, a standard grub's prints `a grub rears back`, a brute's prints `a brute rears back`, each at the same moment as the current message (±1 frame) and once per wind-up.
- V-b. The `cue:` line, `~` line, wind-up time, lunge time and every other output line are byte-identical to the current build in the same scripts, apart from the message words.
- V-c. A script with `when text "rears back" then ...` reacts to all three variants as before.
- V-d. Criteria 1–11 and 17–21 of `combat.md` still hold. No bot result changes. If the bots key on the old message text, the Build step updates them (test tooling).

Experience signal (not for the Playtester's handoff): a text-view player can say, from the message alone, that a runner is the fast, short-warning one and a brute the slow one, and does not report wasted dashes at a distant runner because it "said grub".

Worth doing now: low cost and low risk, but not required by the Goal. Recommendation: build it with the next build that is opened anyway. Do not hold or reopen Review 57 for it. Any change to `play.py` and the tests is a Build step with Verify.

## Open questions

- Whether naming the variant helps the player or only moves the wasted dash to another cue is for the next playtest. Dashing at a distant threat is a reaction-script choice (a rule keyed on a message ignores distance), not a message defect.
- Whether the brute's `a brute rears back` plus its shrug message is enough signal for a human is already open from step 35.
