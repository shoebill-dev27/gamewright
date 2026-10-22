# Combat design addendum, step 68 (stale sentences, manual wording, variant messages)

Status: wording and message strings only. No rule, parameter, timing or room change. Where this file differs from `design/combat.md`, `design/combat-step59.md` or `repo/manual.md`, this file governs. Decisions: D-007 (unchanged), D-011 (accepts and completes D-008).

## 1. Stale sentences, superseded (room 3 in-flight bound)

`design/combat-step-46-room3-cap.md` (amended criterion 11, D-007) governs the cap. These sentences are superseded and must be folded out the next time the files are edited:

- `combat.md`, Cap paragraph: "In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3". Replacement: in rooms 4–5 the count stays at 3 or fewer; in room 3 up to 5 is accepted after a cap delay (2 plus the living spitters).
- `combat.md`, criterion 11: "In rooms 1–5 never more than 3 shots in flight". Replacement: criterion 11 as amended in the step 46 note (a–e).
- `repo/manual.md`, spitter paragraph: "and no more than 3 are in the air at once". Replacement (exact text): "A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once."

## 2. Manual wording for late swipes (step 59, point 1, unchanged rules)

Replace the sentence in the grub warning bullet "or swipe a grub or runner (within 1.5 tiles) to cancel it" with this exact text:

"or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. One swipe is enough to cancel a grub or a runner. A brute is never cancelled."

This covers every point of the step 59 acceptance list.

## 3. Runner cancel vs kill

No separate runner cancel rule is intended. A runner has 1 hp, so a swipe in reach kills it. A late swipe on a runner in reach is therefore a kill, not a cancel, and QA cannot and need not distinguish them. Criterion 6 for the runner reads: an in-reach swipe during wind-up kills it with no lunge.

## 4. Variant messages (D-011; supersedes the message table in step 59 point 2)

| Variant | Mark | Wind-up message | Hit message |
|---|---|---|---|
| Standard grub | `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner grub | `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute grub | `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | n/a | unchanged | `YOU ARE HIT by a shot` (unchanged) |

Rules:
- All three wind-up messages contain `rears back`. Rules keyed on `text "rears back"` match all variants. Rules keyed on `a grub rears back` or `by a grub` match only the standard grub after the change.
- The hit message keeps its current hearts suffix. Only the noun changes.
- Applies in the player view and any other text view that prints these strings. The `cue:` line, `~` line, all timings, the swipe, kill and shrug messages, and spitter messages are unchanged.
- Graphical presentation is not affected.
- Tests and bots that match the old strings are updated by the Build.

Acceptance (verification), at 30 and 60 FPS, practice room, one case per variant:
- V-a. Each wind-up prints its message once, at the same moment as today (±1 frame).
- V-b. A hit by each variant prints the matching hit message on the frame of contact, with unchanged hearts text.
- V-c. All other output is byte-identical to 0.6.1 in the same scripts, apart from these words.
- V-d. `text "rears back"` reacts to all three variants.
- V-e. Criteria 1–11 and 17–21 of `combat.md` hold. No bot result changes.

Experience signal (Review and playtest, not for the Playtester's handoff): a text-view player can say from the message line which kind of grub is attacking or hit them.

## Open questions

- Whether the variant name changes behaviour or only moves a wasted dash is for the next playtest.
- Build timing: only after Review 65, stating the build number if a playtest follows (D-009 item 5).
