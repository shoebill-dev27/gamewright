---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-15
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): when an action player from the project's player profile plays through combat encounters, the fights feel varied and engaging, and the player's moment-to-moment choices (positioning, timing, enemy behavior) visibly matter. The player no longer experiences the fights as the same repeated pattern.

Out of scope: adding input buttons beyond attack, dash and pause (D-001, Owner approval needed); changes to the run length or the non-combat systems; numeric targets (these belong to Design as acceptance criteria, and the final verdict to Review).

No immediate escalation: the Goal does not conflict with the vision or D-001, and it needs no reinterpretation. Improving depth through positioning, timing and enemy behavior is what pillar 1 asks for.

## Unknowns

- Observe (playtester, qa): done (02, 08, 06, 15, 58, 70, 77, 83). Still unobserved in play (suite only): distance-4 idle run, AC-3, 9 dodge, 10, 12, 28(c); real-room clear/heal/next room and "run complete" (AC-13, 14); `z/Z` glyphs; colour.
- Diagnose, Decide: done (03, 53; D-002, D-005, D-006, D-011). A4 (120° cone), D1 (facing mechanic) and D2 (room 1 composition) are held with revisit triggers in 59. Re-entered as 14c (85) on the room-1 play findings in 84 (lethality when flanked, stun in the open window, sameness, no facing indicator). Second re-entry: if it adds nothing measurable, route to `game-director`.
- Design: spec done (59, 60, 65, 73; D-011…D-015, AC-19…AC-30, V-9…V-18). Final V-15 manual wording is in 73 for the Owner. Optional designer edit (from 80): mirror the lunge-draw carve-out in AC-17 and rule 6, and the "after the knockback ends" reading of AC-28(b); not blocking. Dash-draw wording in `combat-visuals.md` (from 83) goes to the art-director in 13i.
- Plan: skipped (Waiting behavior local, per 67). Reopen with the Technical Director if a criterion fails verification a second time.
- Build: AC-19…AC-30 built (67, 75), D-014 rulings built. `test_line_words_match_the_next_draw` is weaker than AC-30(c) (77); a tightening is optional.
- Verify: 13f (77) and 13h (83) QA: no failing criterion at 30/60 FPS; V-17 defeat and dash-off draws pass. 13g art-director (80): V-9…V-14, V-16, V-18 pass; D-015. Open: 13i art-director reading of V-17 and the dash-draw delay (87); AC-15 suite run and V-15 text (Owner); V-6 colour and reverse-video cell not checkable in a text view, record as not checked.
- Play: 14 (84) saw room 1 only, in three blind scripted sessions, all ending in defeat; no spitter, no later rooms; the fights read as uniform. Monotony across rooms is still unjudged. 14b (86): fresh playtester starting directly in rooms 3–5. If 14b cannot reach them either, escalate to the Owner (live play, or Review without them).
- Review: `game-director` with `review-outcome`, planned after 14b, 14c and 13i. Open: run progression after "run over"; F1, F4, F6, F7; numbering of same-type enemies in one cell; A4, D1, D2.
- Skipped: none.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 02-playtester-to-game-designer.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-game-designer-to-game-director.md |
| 3a | Decide | game-director | make-decision | done | 05-game-director-to-studio.md |
| 3b | Observe (defects) | qa | reproduce-defect | done | 06-qa-to-game-designer.md |
| 3c | Observe (rooms 4–5) | playtester | playtest-session | done | 08-playtester-to-game-designer.md |
| 4 | Design | game-designer | write-design-spec | done | 10-game-designer-to-studio.md |
| 5a | Plan | technical-director | technical-plan | done | 14-technical-director-to-studio.md |
| 5b | Observe (spit line) | qa | reproduce-defect | done | 15-qa-to-studio.md |
| 5c | Design (visuals) | art-director | visual-review, write-design-spec | done | 16-art-director-to-studio.md |
| 6a | Build (code) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md |
| 6b | Build (`run_tests` check, manual placed) | gameplay-engineer | implement-change | done | 23-gameplay-engineer-to-studio.md |
| 7a | Verify | qa | verify-change | done (question, no AC failed) | 26-qa-to-studio.md |
| 7b | Verify (visuals) | art-director | visual-review | done (question, no build output) | 27-art-director-to-studio.md |
| 7c | Verify (rerun: manual, runs, captures) | qa | verify-change | done (question, no AC failed) | 29-qa-to-studio.md |
| 7d | Verify (visuals, from captures) | art-director | visual-review | done (fail: V-1, F3) | 32-art-director-to-studio.md |
| 7e | Design (F1 overlap, AC-15 wording) | game-designer | write-design-spec | done | 33-game-designer-to-studio.md |
| 7f | Build (F1/F3 render, manual paragraph) | gameplay-engineer | implement-change | done (render built) | 35-gameplay-engineer-to-studio.md |
| 7f-O | Owner: place the manual paragraph | owner | — | done (Option A, D-007) | 36-studio-to-owner.md |
| 7g | Verify (all but AC-15) | qa | verify-change | done (pass) | 37-studio-to-qa.md |
| 7i | Verify (AC-15, `ManualTest`) | qa | verify-change | done (question: ManualTest blocked) | 38-studio-to-qa.md |
| 7i-O | Owner: `ManualTest` result | owner | — | done (Option A, D-008: 39/40) | 42-studio-to-owner.md |
| 7h | Verify (visuals) | art-director | visual-review | done (pass; V-6 from code, V-7 not seen) | 41-studio-to-art-director.md |
| 7j | Design (`run over` manual test failure) | game-designer | write-design-spec | done (test too literal, D-009) | 43-studio-to-game-designer.md |
| 7k | Build (test fix, line wraps) | gameplay-engineer | implement-change | done (test changed, suite not run) | 46-studio-to-gameplay-engineer.md |
| 7k-O | Owner: place manual text | owner | — | skipped (manual unchanged, D-009) | — |
| 7l-O | Owner: AC-15 rerun | owner | — | done (Option A, D-010: 40/40) | 48-studio-to-owner.md |
| 7l | Verify (AC-15 rerun by QA) | qa | verify-change | skipped (Owner's 40/40 run, D-010) | — |
| 8 | Play (room 1) | playtester | playtest-session | done (room 1 only, scripted, 2 defeats) | 49-studio-to-playtester.md |
| 9a | Diagnose (Play findings) | game-designer | diagnose-experience | done (A1–A3, A5, B, C, D held) | 51-studio-to-game-designer.md |
| 9b | Play (parts not yet seen) | playtester | playtest-session | done (thin: room 2 only, 1 script) | 52-studio-to-playtester.md |
| 10a | Observe (open facts, bots) | qa | reproduce-defect | done (6 facts settled, 2 partly; D-58-1 ruled in 59) | 55-studio-to-qa.md |
| 10b | Design (A1–A3, A5, manual draft) | game-designer | write-design-spec, make-decision | done (spec, D-011, manual draft) | 56-studio-to-game-designer.md |
| 10c | Design (visuals: "on you", hit source) | art-director | visual-review, write-design-spec | done (V-9…V-17, D-012) | 57-studio-to-art-director.md |
| 10-O | Owner: place manual draft (59) and V-15 text | owner | — | open (final V-15 wording now in 73; asked again in 79) | 79-studio-to-owner.md |
| 11 | Plan | technical-director | technical-plan | skipped (Waiting behavior local, per 67; reopen if Verify disagrees) | — |
| 12 | Build (first attempt) | gameplay-engineer | implement-change | done (question: no repo files; Q1 gap) | 61-studio-to-gameplay-engineer.md |
| 12a | Design (Q1 knockback at distance 0, Q2, 3 passages) | game-designer | write-design-spec | done (D-013, AC-28) | 64-studio-to-game-designer.md |
| 12b | Build (re-issue with repo files) | gameplay-engineer | implement-change | done (AC-19…AC-28 built; suite re-run needed) | 66-studio-to-gameplay-engineer.md |
| 13a | Verify | qa | verify-change | done (fail: AC-17, AC-22 suite, AC-28b at 30, V-14/16; V-15 manual) | 70-qa-to-studio.md |
| 13b | Verify (visuals) | art-director | visual-review | done (question: no live view; V-15 fails on document) | 71-art-director-to-studio.md |
| 13c | Design (cell rule at .5, "on you", hit-line word) | game-designer | write-design-spec, make-decision | done (D-014, AC-29/30, V-18) | 73-game-designer-to-studio.md |
| 13d | Build (suite test, D-A, D-C, 13c rulings) | gameplay-engineer | implement-change | done (rulings built; 2 ManualTest need Owner run) | 75-gameplay-engineer-to-studio.md |
| 13e-O | Owner: run suite with manual.md (AC-15) | owner | — | open (parallel to 13i, 14b, 14c) | 79-studio-to-owner.md |
| 13f | Verify (rerun; verbatim captures for AD) | qa | verify-change | done (pass: no failure; AC-15, V-15 open) | 76-studio-to-qa.md |
| 13g | Verify (visuals, from QA captures) | art-director | visual-review | done (pass; V-6, V-15, V-17 open; D-015) | 80-art-director-to-studio.md |
| 13h | Verify (V-17 defeat and dash-off captures) | qa | verify-change | done (pass at 30/60 FPS; dash-draw wording noted) | 82-studio-to-qa.md |
| 13i | Verify (visuals, V-17 and dash-draw wording) | art-director | visual-review, make-decision | open (parallel to 14b, 14c) | 87-studio-to-art-director.md |
| 14 | Play (room 1, fresh playtester) | playtester | playtest-session | done (thin: room 1 only, 3 scripted sessions, all defeats) | 81-studio-to-playtester.md |
| 14b | Play (rooms 3–5, started directly) | playtester | playtest-session | open (parallel to 13i, 14c) | 86-studio-to-playtester.md |
| 14c | Diagnose (room-1 findings from 84, held items) | game-designer | diagnose-experience | open (parallel to 13i, 14b) | 85-studio-to-game-designer.md |
| 15 | Review | game-director | review-outcome | planned (after 13i, 14b, 14c) | — |

## Route changes

After 13h (83): V-17 passes in both cases at 30 and 60 FPS; 13i opened (87) for the AD's reading and the dash-draw wording. After 14 (84): thin again (room 1 only, 3 defeats); its experience issues go to Diagnose 14c (85), and a fresh Play 14b (86) starts directly in rooms 3–5. No escalation.

## Next action

- `game-designer` runs 14c from `85-studio-to-game-designer.md`, addressed to `studio`.
- `playtester` runs 14b from `86-studio-to-playtester.md` (fresh executor, build and profile only), addressed to `studio`.
- `art-director` runs 13i from `87-studio-to-art-director.md`, addressed to `studio`.
- Owner (13e-O, 10-O, still open): see `79-studio-to-owner.md`: run the suite with `manual.md` beside `repo/`, report the count, and place the V-15 text from 73.
- Then Route after all three. Defects raised by 14c go to `qa`. Design or experience issues follow the return rules (a direction change goes to `game-director`). If 13i asks for a new draw event, go to Design. If 14b again cannot reach rooms 3–5, escalate to the Owner. Otherwise go to Review (15).

## Outcome

(Filled at Close.)
