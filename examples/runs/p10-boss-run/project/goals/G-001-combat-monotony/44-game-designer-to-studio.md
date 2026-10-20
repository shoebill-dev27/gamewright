---
kind: handoff
goal: G-001
seq: 44
from: game-designer
to: studio
stage: Design
outcome: done
---
# 44: game-designer → studio — Criterion 13 ruling: walker limit 3–7 at 60 FPS, no build change

## Task

Pass the ruling on criterion 13 to QA, who is verifying build 0.6 in parallel (41), so QA judges the walker figures against the amended limits. No build change is needed. No Director decision is needed.

## Context

G-001 (combat monotony). Build 0.6 (Design 35 and 38, D-004, D-005) puts the walker bot at 7 hearts lost in rooms 3–5 at 60 FPS (4 at 30 FPS), against criterion 13's limit of 6. Handoffs 40 and 42 contain the figures and the question.

## Findings

**Ruling: 7 hearts is not a breach of intent. The limit of 6 was too tight, and it was a snapshot of the 0.5 result, not a derived bound. The limit changes to 3–7. No room or enemy parameter changes.**

The purpose of criterion 13 is a gradient, and it holds at 7:

- Costly: walker 4 (30 FPS) and 7 (60 FPS) hearts lost, against dodger 0 lost, 3/3 cleared and 7 or more dashes per room, and camper 0 of 3 cleared.
- Not hopeless: the walker clears 2 of 3 at both rates.

Why a hearts ceiling below 7 is the wrong tool:

- A room has 3 hearts, and a cleared room costs at most 2. A walker clearing 2 of 3 rooms therefore loses at most 3+2+2 = 7.
- The clear count is what carries "not hopeless". A ceiling of 6 only forbids a particular distribution of hearts across rooms.
- The walker's 0.15 s grid sensitivity moves single hearts between rooms with no player-visible cause (criterion 16d). The engineer saw the room totals move in opposite directions between 0.5 and 0.6.

Why no parameter changes: the shift is the expected net of D-004 (brute not cancelled: more losses) and D-005 (consumed shots: fewer). A parameter change would fit one bot's grid phase and force re-verification of criteria 11, 13, 14, 15, 18, 20 and 21.

Changed criteria:

- **13:** the walker's upper limit is 7 (was 6), and the lower limit 3 stays. The clears-at-least-2 gate is now the primary one. The dodger, camper and per-rate rules are unchanged.
- **13e/f:** per-room walker numbers are not criteria. The rates are checked separately.
- **13 reporting rule:** QA reports only values that fail 13a–d.
- Criteria 14, 15 and 16 are unchanged.

Full amended text: `design/combat-step-44-walker-limit.md`, which governs where `combat.md` differs. `combat.md` itself was not rewritten, so it still shows the old numbers until the two are merged.

**Build change list: none.** `bots.py` is unchanged. The engineer already removed the walker's upper bound of 6 from its own test. Its test should now assert 3 to 7 hearts lost and at least 2 rooms cleared, per rate. That is test tooling and not a build change.

**Does the answer depend on QA's figures?** Yes, in a limited way. These results would reopen the ruling:

1. The walker clears fewer than 2 of 3 rooms at either rate. That means walled out, and the response would be a parameter change.
2. The walker loses fewer than 3 hearts at either rate. The 30 FPS margin is only 1 heart.
3. The dodger loses more than half the walker's total, or fails 3/3.
4. The camper clears as many rooms as the walker or more.
5. A rate difference that comes from a rule and not from bot timing, which is a build defect (16e).

A QA 60 FPS walker figure of 6 or 7 with 2 rooms cleared changes nothing.

QA re-verifies only criterion 13 against the amended limits, at both rates, on the unchanged build. It also confirms the walker's rate differences come from the 0.15 s grid.

## Decisions already made

- D-001: one-button combat.
- D-004 and D-005: unchanged and respected.
- D-006 (new): the walker limit in rooms 3–5 is 3–7 hearts with at least 2 rooms cleared, and no parameter change.

## Constraints

- Nothing in the 30 and 60 FPS behavior changes.
- No new enemy, healing, input or room content.
- Hand-timed playtest of rooms 3–5 remains the real test of "costly but not hopeless" for a human. If a cue-ignoring human cannot get through, reopen D-006 and the D-004/D-005 tuning values.

## Open questions

- For QA: does `play.py` print "the brute shrugs off the swipe" for the `shrug` event? Handoff 40 could not check it, and this note does not change that.
- For the Studio: fold `design/combat-step-44-walker-limit.md` into `design/combat.md` at the next edit of that file, so that criterion 13 is stated in one place.

## Expected output

The Studio forwards this ruling to QA to use when judging the criterion 13 figures. The ruling needs no further Design work unless one of the five listed results appears. If one does, route it back to `game-designer`, or to `game-director` if it touches D-004, D-005 or scope.

## Sender assessment

High confidence in the ruling. It is a derivation from the 3-hearts-per-room structure and from the stated purpose of the criterion, not a measurement. I did not run the bots, because the ruling depends on the structure and the engineer's figures. QA's independent figures can break it only through the five results above. The weakest margin is the lower limit at 30 FPS (4 against 3).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Previous handoff: goals/G-001-combat-monotony/42-studio-to-game-designer.md
