# Goal log

One entry per Intake, Route and Resume, appended by whoever runs the operation. Entries are never edited.

## Before the log

- Intake check (Route step 4) on 01: the first draft told the Playtester the Owner's report and
  asked "where do players stall", which primes the observation. Rewritten with a neutral play focus
  (levels 1–3) and the Owner's report withheld. Load narrowed to `project.md#player-profile`.
- Route after step 1 (`02-playtester-to-game-designer.md`): the outcome fits the plan (two of three
  children stalled 20–35 s at the start of level 1; the report is observation only). No escalation
  trigger fires, and no `tentative` stage exists to confirm or drop. Added step 2b: `art-director`
  `visual-review` in parallel with step 2, as the Intake note reserved for this point. The report
  contains visual facts (tide pool in the same pastel tone as the sand; crab with a darker outline
  that bobs; two of three children touched the crab first), so the cause may be visual. Steps 2 and
  2b are independent (both read only the observation), so they run in parallel and Route waits for
  both before step 3. Step 2's handoff was completed at Route: the Owner's words, the success
  condition, the out-of-scope list and the text-constraint flag were added (the `game-designer` did
  not have them); `project.md#vision`, `#constraints`, `#player-profile`, `design/onboarding.md` and
  D-001 were put in its Load. Not added: a `qa` Observe step. The playtester reported the missing
  response to taps on the crab and the home as observed; whether that contradicts the design
  documents is for step 2 to say, and if it does, the return rules send that part to `qa`.
  Step 3 may need `art-director` for what the player sees; decide after step 2 and 2b.

## 005-route · 2026-10-12

Status: active. Open: 06-studio-to-game-designer.md.

After steps 2 and 2b: the diagnoses agree (pool lacks affordance, crab is a false affordance, silent touches, text-only teaching), so the plan holds. Design (3) is open for `game-designer`, who adopts the art-director's visual direction. Idle hint (Option C) is barred from the spec because it touches D-001; if wanted, route Decide. Plan is re-asked after Design. No `qa` Observe: Verify covers touch response.

## 007-route · 2026-10-12

Status: active. Open: 08-studio-to-gameplay-engineer.md.

After step 3 (07): the spec is written in `design/onboarding.md` (options A + B, no Option C). Plan is skipped: the change is local to level 1. Build (4) is open for `gameplay-engineer`. Verify must be addressed to `studio` so a fresh Playtester handoff can be composed afterward. The intro-motion vs D-001 judgment is left for Review.

## 009-route · 2026-10-12

Status: active. Open: 09-gameplay-engineer-to-game-designer.md.

After step 4 (09): Build held and handed back `question` — the spec does not define a non-pool touch during the intro or the intro's relation to undo (plus minor gaps Q3–Q6). Per the return rules (Build, spec ambiguous) Design reopens as 3d for `game-designer`, then Build resumes (4b). No escalation; nothing was built.

## 011-route · 2026-10-12

Status: active. Open: 11-studio-to-gameplay-engineer.md.

After step 3d (10): the designer settled Q1–Q6 in `design/onboarding.md` and D-002; no spec gap remains and the 0.2 s criterion is unchanged. Plan stays skipped. Build resumes (4b) with a Handoff addressed to `studio`; QA also gets the 12 checks and the platform reduced-motion check. No escalation.

## 015-route · 2026-10-12

Status: active. Open: 13-studio-to-qa.md.

After step 4b (12): Build is done; the engineer found no further spec gap, so the plan holds and Plan stays skipped. Verify (5) is open for `qa` with a fresh Handoff (13) that omits the Sender assessment. It carries the 12 checks as exercise aids, plus the platform reduced-motion check and the home-styling capture. The report goes to `studio` so a clean Playtester handoff can be composed.

## 017-route · 2026-10-12

Status: active. Open: 15-studio-to-game-designer.md.

After step 5 (14): all 12 checks pass, but QA found a spec gap (G1: sand taps 0.6–1.5 s after a pulse get no response, against "no silent touches") plus notes N1–N4. Expected behavior is undefined, so Design reopens as 3e (game-designer) before Play, since a spec change would alter the build the Playtester sees. Build/Verify re-run only if the spec changes; Play stays planned.

## 019-route · 2026-10-12

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After step 3e (16): the designer settled G1 and N1–N4 in spec revision 2 and D-003. Player-facing behavior changed (sand-tap blip, larger pool hit area, crab flip target, pulse precedence), so Build 4c is open and Verify 5b is confirmed (checks 1–16). Play stays after 5b. Plan stays skipped; no escalation.

## 021-route · 2026-10-12

Status: active. Open: 19-studio-to-game-designer.md.

After step 4c (18): Build held with `question` — a sand tap during the 0.15 s ease-back (pending pulse) is undefined; also the 1.5 s window origin and a held-pool second finger. Spec ambiguous, so Design reopens as 3f (game-designer); Build resumes as 4d, then Verify 5b (checks 1–16). Items 2–5 stay settled. Plan stays skipped; no escalation.

## 023-route · 2026-10-12

Status: active. Open: 21-studio-to-gameplay-engineer.md.

After step 3f (20): the designer settled the ease-back sand tap, 1.5 s window origin and held-pool second finger in spec revision 3 and D-004; no spec gap remains. Build resumes as 4d (item 1 changed, items 2–5 as planned), then Verify 5b with checks 1–18. Plan stays skipped; no escalation.

## 026-route · 2026-10-12

Status: active. Open: 23-studio-to-qa.md.

After step 4d (22): Build is done as build 0.4 (spec revision 3, items 1–5); the engineer found no spec gap, so Plan stays skipped and nothing escalates. Verify 5b is open for `qa` with a fresh Handoff (23) that omits the Sender assessment and lists checks 1–18 (4, 13, 17, 18 new or changed). The report goes to `studio`; Play and Review stay planned.

## 028-route · 2026-10-12

Status: active. Open: 25-studio-to-game-designer.md.

After step 5b (24): 17 of 18 checks pass; check 4 fails under reduce-motion (a sand tap 0.4–0.6 s after a pulse start is silent). Spec rule 5's 0.6 s window conflicts with the 0.4 s reduce-motion pulse, so the mechanism is a design choice: Design reopens as 3g (game-designer), then Build 4e and Verify 5c. First failure of check 4, so no Plan; no escalation. Play and Review wait for the corrected build.

## 030-route · 2026-10-12

Status: active. Open: 27-studio-to-gameplay-engineer.md.

After step 3g (26): the designer chose the reduce-motion mechanism (0.6 s two-beat brightness pulse, spec revision 4, D-005) and found no other silent window. Default-mode behavior is unchanged. Build 4e is open for `gameplay-engineer` (27), then Verify 5c (checks 1–20; 19 and 20 new). Plan stays skipped; no escalation.

## 033-route · 2026-10-12

Status: active. Open: 29-studio-to-qa.md.

After step 4e (28): Build is done as build 0.5 (spec revision 4, changes 1–5); the engineer found no blocking spec gap, so Plan stays skipped and nothing escalates. Verify 5c is open for `qa` with a fresh Handoff (29) that omits the Sender assessment and lists checks 1–20 (19 and 20 new). Play and Review stay planned.

## 035-route · 2026-10-12

Status: active. Open: 31-studio-to-game-designer.md.

After step 5c (30): QA passed checks 1–20 on the build record but found spec gap SG-1 (sand tap after a pool touch cancelled a pulse, before P+0.6 s: no defined response, yet check 4 requires one) and a check 20 wording mismatch (O1). Expected behavior is undefined, so Design reopens as 3h. Build 4f and Verify 5d are tentative on a behavior change. Play waits for a settled build. No escalation.

## 038-route · 2026-10-13

Status: active. Open: 33-studio-to-gameplay-engineer.md.

After step 3h (32): the designer ruled SG-1 (a blocked sand tap after a pulse cancelled by a pool touch gets the blip, both modes; spec rev 5, D-006). Player-facing behavior changes, so Build 4f is confirmed and open (33), and Verify 5d is now planned. O1 and O3 are wording or accepted; no escalation, Plan stays skipped.

## 041-route · 2026-10-13

Status: active. Open: 35-studio-to-qa.md.

After step 4f (34): Build is done as build 0.6 (spec revision 5, SG-1 change; build record wording fixed). No spec gap or question came back, so Plan stays skipped and nothing escalates. Verify 5d is open for `qa` (35) with the Sender assessment left out. Play and Review stay planned.

## 043-route · 2026-10-13

Status: active. Open: 37-studio-to-playtester.md.

After step 5d (36): QA passed checks 4, 13, 18, 19, 20, 21 on build 0.6 with no failure, regression or blocking spec gap, so the plan holds. Play 6 is open for `playtester` (37), a fresh Handoff with the build and player profile only. The two low-severity record wording notes are carried to Review / Close, not sent back to Build. No escalation.

## 045-route · 2026-10-13

Status: active. Open: 39-studio-to-game-director.md.

After step 6 (38): the playtester found the main path (touch the pool) clear and responsive. The issues named are secondary and no defect was reported, so there is no return to Diagnose or Observe. Review 7 is open for `game-director` (39) with the report, QA results and open items. No escalation.

## 047-route · 2026-10-13

Status: done. Open: none.

After step 7 (40): `game-director` ruled goal-met on simulated evidence (QA record check and a playtester read-through, no device, no real children). The playtest issues are secondary and concern play after the first interaction, so they become proposed Goals, not a return to Diagnose. No direction change, no escalation. Close (8) done.
