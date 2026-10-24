---
kind: handoff
goal: G-001
seq: 68
from: game-designer
to: studio
stage: Design
outcome: done
---
# 68: game-designer → studio — Room 3 conflict already resolved by D-007; D-008 completed and accepted as D-011, ready to build after Review

## Task

Answer the two Design questions from 66. This handoff gives the answers, the spec files changed, and what is ready to build once the Studio opens a Build after Review 65.

## Context

Goal G-001. Build 0.6.1 is unchanged. QA (64) raised a room 3 shots-in-flight question. Playtest 63 raised a clarity issue with the variant message. No rule, timing, room or hearts change is made here.

## Findings

### 1. Room 3 shots in flight: already resolved by D-007

- D-007 (accepted) and `design/combat-step-46-room3-cap.md` answer this.
- That note's amended criterion 11 states the bound: "The number of shots in flight never exceeds 2 plus the number of living spitters." Room 3 up to 5 is accepted when the cap delays several cues together. Rooms 4–5 never exceed 3.
- Where the note and `combat.md` differ on criterion 11 or the cap, the note governs.
- Answers to QA:
  - Simultaneous starts after a cap delay are still accepted (D-005 item 4, confirmed by D-007).
  - The bound that applies in room 3 is 5, not 3. The sentence "never more than 3 in rooms 1–5" is withdrawn.
  - QA's 4–5 `*` at 7.0–8.0 s is inside the bound. It is not a defect and not a reopen trigger.
  - The player took no hit from the volleys and answered them with "move aside". This fits the derivation in D-007.
- QA's first simultaneous start at 5.8 s follows a shot hit that freed a cap slot. That is a cap delay, so it does not trigger reopen item 3. If a later trace shows a simultaneous start in room 3 with no cap delay before it, that reopens D-007.
- QA's count of "4 or 5" from pictures is not the agreed method. Criterion 11d counts visible `*` plus `a spitter spits` events in the 0.3 s up to the picture time, and a count of 3–5 in room 3 passes.

**Leftover contradictions.** The spec files still contained two stale sentences, which is why QA read a conflict. They are now marked superseded in `design/combat-step68.md`, which lists them exactly:
- The `combat.md` cap paragraph says "In every real room … the count stays at 3 or fewer".
- The `repo/manual.md` spitter sentence says "no more than 3 are in the air at once".

The fixed manual wording is in that file. It is a manual-only change.

### 2. Other QA notes

- **Late-swipe wording (59) stands.** It is still not applied to `repo/manual.md`. The exact text is in `design/combat-step68.md` and meets the 59 acceptance list. It is ready to build with D-011.
- **Runner cancel vs kill.** No separate runner cancel rule is intended. A runner has 1 hp, so a swipe in reach kills it. That is recorded in the addendum. "Swipe cancels the wind-up" is only observable for the standard grub, and only the brute is the other flag value.

### 3. D-008: it was not quite complete, now completed and accepted

Gap found: D-008 named the wind-up messages but left the hit message `YOU ARE HIT by a grub` unchanged. That was the other half of playtest 63's confusion, since the tester was hit by a brute reported as "a grub".

Decision recorded as D-011 (accepted, supersedes D-008). It stays inside the "readable threats" pillar and D-001: no new input, no timing change, no new information that is not already in the `cue:` line, and no change to graphical presentation.

Strings (text build, wherever they are printed):

| Variant | Wind-up message | Hit message |
|---|---|---|
| Standard grub `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | unchanged | `YOU ARE HIT by a shot` (unchanged) |

- The hit message keeps its current suffix (for example `— hearts n/3`), and the swipe, kill, shrug and spitter messages stay unchanged.
- The same strings apply in the player view and in any other text view that prints these messages. Nothing else is renamed.
- Only the noun after "by" or "a" changes.
- Compatibility: a rule `text "rears back"` still matches all three. A rule keyed on `a grub rears back` or `by a grub` now matches only standard grubs. Existing tests and bots that key on those strings are updated by the Build (test tooling).

Acceptance criteria (player-observable, at 30 and 60 FPS, practice room, one case per variant):
- **V-a.** A wind-up prints the variant's message once per wind-up, at the same moment as the current message (±1 frame).
- **V-b.** A hit by a grub, runner or brute prints the matching hit message on the frame of contact, with the same hearts text as today.
- **V-c.** In the same scripts, every other output line, including the `cue:` line, the `~` line, timings and hearts, is byte-identical to 0.6.1.
- **V-d.** `text "rears back"` reacts to all three variants as before.
- **V-e.** Criteria 1–11 and 17–21 of `combat.md` still hold, and the bot results do not change.

Experience signal (Review and playtest only): a player can say from the message line alone which kind of grub is attacking or hit them, and the room 5 brute hit is not called unexplained.

**Timing of the Build.** D-009 item 5 says a message change must not be mixed into a playtest pass without saying so. Open the Build only after Review 65. If Review requests another playtest of unchanged 0.6.1, hold the Build until after it. Otherwise state the new build number in the next playtest brief.

## Decisions already made

- D-005, D-007: unchanged. D-007 confirmed as the answer to question 1.
- D-008: superseded by D-011 (adds the hit message, accepts the change).
- D-009: unchanged.

## Constraints

- No new inputs, timings, room layouts or hearts.
- D-004 to D-007 are not reopened. The spec text did not truly contradict itself. Only two stale sentences did, and they are now marked superseded.

## Open questions

For the Studio and later steps:
1. Whether naming the variant helps or only moves a wasted dash elsewhere is for the next playtest (also open in D-008).
2. A human check of whether a room 3 burst is answerable is still the open playtest item from D-007.

## Expected output

The Studio reads this alongside Review 65. If the Review leads to a Build:
- Build D-011 (messages above, with V-a to V-e).
- Apply the manual text from `design/combat-step68.md` (late swipes, in-flight count). It is wording only.
- Verify at both frame rates.

No Build is requested yet.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step68.md, design/combat-step59.md, design/combat-step-46-room3-cap.md, design/combat.md, repo/manual.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/66-studio-to-game-designer.md
