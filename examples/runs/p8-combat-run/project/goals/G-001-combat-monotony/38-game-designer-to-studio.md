---
kind: handoff
goal: G-001
seq: 38
from: game-designer
to: studio
stage: Build
outcome: done
---
# 38: game-designer → studio — Rulings on blocked contact and simultaneous cue starts; complete change list for Build 0.6

## Task

Route the Build step for 0.6. The spec in `design/combat.md` (marked "step 38") is complete for Build: the step 35 items plus two rulings on QA's open items (handoff 36). No further design step is needed first.

## Context

G-001 (combat monotony). Step 35 specified the cue gap in rooms 4–5, the brute that is not cancelled by a swipe, and the manual wording (D-004). QA (handoff 36) found build 0.5 conforming to the 0.5 spec and reported two undefined behaviors. Both are ruled here. No scope or pillar change, no new input, no new enemy, no healing. Contact sampling (D-002, D-003) is unchanged.

## Findings

**Ruling 1 (QA item 1): a shot that touches an invulnerable player is consumed (D-005).**
- Rule: a shot with contact (distance <= 0.4, unchanged) on a player who cannot be hurt (dash, 0.3 s hit-stun, or hurt window until 0.8 s after the hit) disappears on that frame with no damage. It does not pass through and does not wait for the window to end.
- Lunges: a lunge has one hit; a contact on a protected player spends it. No damage from that lunge for the rest of it, even if the protection ends while the grub is still in reach. The lunge is not cancelled or shortened (existing rule). The next lunge damages normally.
- Why: QA saw damage land exactly at the end of the hurt window (4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS), 0.15–0.2 s after the shot visibly reached the player. That is a hidden hit, against "every threat is visible before it can hurt". The mechanism is QA's hypothesis, not confirmed in code; the rule holds regardless.
- Difficulty: only the chained hit on an already hurt player disappears, so rooms 4–5 get somewhat easier in that case. The intended cost (a still player takes each shot that arrives after the window) stays. Tuning values (offset, interval) are the lever if the rooms get too easy.
- Dash: a shot or lunge the dash overlaps cannot hit after the dash ends, so the dash is a more robust answer. It is not made necessary.
- Observable criterion for QA: criteria 20 (shots: hurt window, dash, normal hit, room 4 still-player trace, cap slots, band unchanged) and 21 (lunges: dash, hurt window, lunge not cancelled, next lunge normal). Numbers are in `design/combat.md`.

**Ruling 2 (QA item 2): a simultaneous cue start is accepted in room 3 and practice rooms; the gap rule is not extended (D-005).**
- Reasons: reproduced only in a practice replica with a surviving player, not in a real room; room 3's verified first shots (1.8, 2.6, 3.4 s) are unaffected either way; two simultaneous cues are two readable lines each answered by a sidestep or a dash; rooms 4–5 are covered by the rule.
- Criteria 11 and 18 do not change for room 3 and practice rooms. Criterion 18d must use room 4 or 5 (the practice room does not use the rule), or QA says d was not run. Revisit if a real-room trace of room 3 shows a problem.

**Bot expectations (questions 3 and 4).**
- Criterion 13 (walker 3–6 hearts, ≥2 of 3 cleared; dodger ≤ half, 3/3; camper fewer than walker): numbers kept. Two opposite effects on the walker in rooms 4–5: the brute lunge it used to cancel (step 35, more hearts) and the consumed shots (step 38, fewer hearts). Net unknown, and the walker's lower limit of 3 is now also at risk. Measured on 0.6; values outside limits are reported to `game-designer` as tuning, not as a build defect.
- Criterion 14 (grub rooms): numbers kept. Rooms 1–2 have no spitters; the lunge ruling can only lower hearts. The step 35 rule for the dodger's brute policy stands (sidestep or dash on the cue, swipe only in recovery); the Build step checks `bots.py`.
- Criterion 15 (dodger dashes ≥1 in rooms 3–5): numbers kept; the dash is safer, not required; a missing dash is reported, nothing is forced.
- Inconsistencies fixed in the spec: "two shots arriving together" now says the second is consumed; "dash invulnerability stops the damage" and "hurt invulnerability" now cover spent lunges; criterion 3 notes no later damage; criterion 16a/16e include 20 and 21 (and the band note); cap and edge-case notes added. Criteria 6, 11, 18 and 19 are unchanged in substance (11 and 18 only gain a note). Manual wording from step 35 is not made inconsistent; two lines are added below.

## Decisions already made

- D-001 (attack and dash only), D-002 and D-003 (contact sampling and exact reach; unchanged), D-004 (cue gap rule and offset in rooms 4–5, brute flag, Option 3 deferred; unchanged), D-005 (this step: consumed shots, spent lunge, simultaneous start accepted outside rooms 4–5).

## Constraints

- Correct at 30 and 60 FPS, all durations on accumulated time. Do not change contact detection (`distance <= reach` per frame after movement). Only the consequence after a detected contact changes.
- Room 3 criterion 11 stays (1.8, 2.6, 3.4 s ±1 frame). No new input, enemy, healing, room content or message beyond those listed.
- A spec step only: nothing was built or run. The bot numbers for 13–15 on 0.6 are unknown.

## Open questions

- Is a real-room cap delay reproducible in room 3, and is a simultaneous start a problem there? Needs a real-room trace of 15 s or more with a surviving player (a reaction-rule script as in the manual example). QA can do it in Verify.
- Do the walker's hearts in rooms 4–5 stay inside criterion 13 on 0.6 (the two effects pull in opposite directions)? Answered by the bots on 0.6.
- Is the "hidden hit" mechanism in 0.5 really an unconsumed shot, or something else with the same effect? Build confirms in code; criterion 20a confirms the result.

## Expected output

**Build 0.6** implements the full set below, then QA verifies it, then the bots run, then the hand-timed playtest.

Complete change list for Build 0.6:
1. (Step 35) Spitter offset per room: 0.8 s default (rooms 1–3, practice rooms), 1.2 s in rooms 4–5 (first shots 1.8 and 3.0 s in those rooms).
2. (Step 35) Cue gap rule in rooms 4–5 only: a spitter starts a cue only if no other spitter's cue is running, the last shot in the room was at least 0.6 s ago (1 ms tolerance), and the cap allows it; else wait 0.2 s and check again. A cancelled cue is not a shot. Room 3 and practice rooms do not use it.
3. (Step 35) Brute (`G`) wind-up is not cancelled by a swipe: the swipe deals 1 damage, shows "the brute shrugs off the swipe", the cue and timer continue, the lunge happens at 0.7 s. Kill in wind-up: no lunge, no message. Flag per variant: standard yes, runner yes, brute no.
4. (Step 35) Dodger bot policy against the brute: sidestep or dash on the cue, swipe in recovery only (check `bots.py`).
5. **(Step 38) Shot consumed on any contact:** a shot that makes contact with a player who is dashing, in hit-stun, or in hurt invulnerability is removed on that frame with no damage.
6. **(Step 38) Lunge hit spent:** a lunge that makes contact with a protected player deals no damage for the rest of that lunge; the lunge is not cancelled or shortened; the next lunge is normal.
7. (Step 38) No change to the cue gap rule for room 3, practice rooms, or to contact detection.
8. Manual (`repo/manual.md`), besides the step 35 lines: (a) "A shot that reaches you while you are dashing or still flashing after a hit is stopped and does no damage." (b) "A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection ends during that lunge." Also update the version number; the sentence "A swipe that interrupts a grub's warning staggers it for 0.4 s" needs the step 35 exception for the brute, as in the step 35 handoff.

New and changed criteria for QA: new 20 (a–f) and 21 (a–d); amended 3, 13, 14, 15, 16 (a and e), 11 and 18 (notes only). Existing 18 and 19 from step 35 stay. Scripts for 20–21 are practice-room scripts at `fps 30` and `fps 60`; the derived arrival time of the spitter at (15,4) to a player at (8,4) is about 4.0 s, to be taken from the trace.

For `art-director` (deferred with the other visual criteria until a graphical build exists): (1) step 35 brute hit reaction and the outdated "0.8 s apart" sentence; (2) step 38: a consumed shot should visibly end at the player (small flash or puff), not read as passing through. Nothing in the visual spec is blocked.

## Sender assessment

Confidence is high for the rule (it follows the existing "disappears on contact" text and removes a hidden hit) and medium for the effect on rooms 4–5 difficulty and on bot counts, which are derived and not measured. The rooms may become somewhat easier; the playtest decides, and offset, interval and cap are the levers (D-005). Room 3 simultaneous starts are accepted on the evidence available; the call is reversible. I do not think anything else is needed before Build.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-game-designer.md
