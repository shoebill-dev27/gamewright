# Goal log

One entry per Intake, Route and Resume, appended by whoever runs the operation.
Entries are never edited.

## 001-intake · 2026-10-15

Status: active. Open: 01-studio-to-playtester.md.

Initial route from Intake (pattern 2, experience problem with unknown cause). No changes yet.

## 003-route · 2026-10-15

Status: active. Open: 02-playtester-to-game-designer.md.

After step 1 (Observe): the report fits the plan, so Diagnose follows. Coverage is limited to rooms 1–3 in scripted play. Open items (hit lockout, grub not dying, post-death state) go to the designer to check against design/combat.md; any defect found goes to `qa`.

## 005-route · 2026-10-15

Status: active. Open: 03-game-designer-to-game-director.md, 04-studio-to-qa.md.

After step 2 (Diagnose): fits the plan, so Decide follows. Opened a parallel QA Observe (3b) for the two possible defects; it is independent of Decide. Added a tentative playtester round on rooms 4–5 (3c), to be opened only if the Director asks for it.

## 008-route · 2026-10-15

Status: active. Open: 07-studio-to-playtester.md.

After steps 3a and 3b: the Director chose Option A (D-002) and asked for a rooms 4–5 play round first, so 3c is confirmed and opened (07). QA found spec gaps, not defects; they join the Design step, which is now planned and waits for the 3c report.

## 010-route · 2026-10-15

Status: active. Open: 09-studio-to-game-designer.md.

After step 3c: the rooms 4–5 report fits the plan (no defects, no escalation trigger), so Design is opened (09). The Handoff carries the report, the Director's direction (05) and QA's spec questions (06), plus the missing Skill and Decisions D-001/D-002.

## 012-route · 2026-10-15

Status: active. Open: 11-studio-to-technical-director.md, 12-studio-to-qa.md, 13-studio-to-art-director.md.

After step 4 (Design): the spec fits the plan, no escalation trigger. Plan is confirmed (cross-system, feasibility unchecked) and opened with two independent parallel steps: QA logs the duplicate spit line (12) and art-director reviews the visuals (13). Build, Verify, Play are now planned; Verify adds an art-director visual review.

## 016-route · 2026-10-15

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After steps 5a–5c: plan, QA report and visual spec fit the route; no escalation trigger and no spec problem needs Design. Build opened (17) with all three as inputs; the spit-line fix and the visual spec join Build and Verify (AC-8, V-1…V-8).

## 024-route · 2026-10-15

Status: active. Open: 19-studio-to-gameplay-engineer.md.

After step 6a (18, question): code is done, but `manual.md` (T8) could not be written and QA depends on it (AC-15, V-5). Build is reopened as 6b (19), `manual.md` only, with the draft from 18. A second block on the same write goes to the Owner.

## 026-route · 2026-10-15

Status: blocked-on-owner. Open: 19-studio-to-gameplay-engineer.md.

After step 6b (20, question): `manual.md` was blocked a second time for the same missing write access, with nothing new supplied. Loop limit reached, so the Goal is `blocked-on-owner` and Escalation 21 asks the Owner to place the draft (A), grant write access (B) or skip it (C). Route unchanged.

## 028-resume · 2026-10-15

Status: active. Open: 22-studio-to-gameplay-engineer.md.

Resume after Owner decision D-005 (Option A of Escalation 21): the Owner placed the draft `manual.md` unchanged. The Goal is `active` again. Step 6b is narrowed to a `run_tests` check (22). If it gives 34/34, Verify opens as two parallel steps. The rest of the route is unchanged.

## 030-route · 2026-10-15

Status: active. Open: 24-studio-to-qa.md, 25-studio-to-art-director.md.

After step 6b (23): `run_tests` was 33/34 only because the engineer's workspace lacked `manual.md`; the draft's text is statically consistent. Not an Owner matter, so Verify opens as parallel 7a (QA, also runs `ManualTest` with the manual placed) and 7b (visuals). Rest unchanged.

## 033-route · 2026-10-15

Status: active. Open: 28-studio-to-qa.md.

After 7a/7b (26, 27; both question): no AC failed. QA's `ManualTest` error came from its workspace lacking `manual.md`; the art director had no build output. Verify reruns as 7c: QA (28) checks the manual layout, runs independent scripts and captures raw output. 7d (art director) opens after 7c with those captures. Play and Review unchanged.

## 035-route · 2026-10-15

Status: active. Open: 31-studio-to-art-director.md, 30-studio-to-game-designer.md.

After 7c (29, question): no AC failed. Open as parallel steps: 7d (art director, V-1…V-8 from QA's captures) and 7e (designer rules on F1, grub on the player's tile, and the AC-15 wording). 7f/7g are tentative: only if 7e needs a build change. `ManualTest` stays not run; static check clean, not escalated.

## 038-route · 2026-10-15

Status: active. Open: 34-studio-to-gameplay-engineer.md.

After 7d/7e (32 fail on V-1, 33 done): the designer allowed overlap but never hidden (D-006, AC-18) and reworded AC-15, so Build reopens as 7f (34), with the art director's F3 (enemy over arc). 7g (QA) and 7h (art director) are now planned after it; F2 stays cosmetic.

## 040-route · 2026-10-15

Status: blocked-on-owner. Open: 37-studio-to-qa.md.

After 7f (35, question): render fix built and tested; only the `manual.md` paragraph is missing, a third round with nothing new supplied, so it is escalated (36, Option A recommended). 7g (37) runs meanwhile without AC-15; 7i (AC-15) is tentative on the Owner's answer.

## 042-resume · 2026-10-15

Status: active. Open: 37-studio-to-qa.md, 38-studio-to-qa.md.

Resume after the Owner chose Option A (36, D-007): the Owner placed the manual paragraph. Goal back to `active`. 7i (AC-15, `ManualTest`) is confirmed and opened as 38 in parallel with 7g (37); 7h, Play and Review unchanged.

## 045-route · 2026-10-15

Status: blocked-on-owner. Open: 41-studio-to-art-director.md.

After 7g/7i (39 pass; 40 question): 7g passed, so 7h opens (41). 7i found the paragraph and behavior fine, but `ManualTest` cannot read `manual.md` in the QA workspace, the same missing input as in 29. Per the loop limit it goes to the Owner (42), not QA again. 7h runs meanwhile; Play waits for AC-15.

## 047-resume · 2026-10-15

Status: active. Open: 41-studio-to-art-director.md, 43-studio-to-game-designer.md.

After the Owner chose A (42, D-008): the suite ran 39/40; `ManualTest` fails on the phrase `run over` missing from `manual.md`. Goal back to `active`. 7j opens (43): the designer rules on manual vs. test. 7k, 7k-O and 7l are tentative on that ruling. 7h continues; Play waits for AC-15.

## 050-route · 2026-10-15

Status: active. Open: 46-studio-to-gameplay-engineer.md.

After 7h/7j (44 pass; 45 done): visuals accepted (V-6 from code; V-7 and F4 left to Play and Review). The designer ruled the manual is right and the test too literal (D-009), so 7k opens (46), test only; 7k-O is dropped and 7l is planned. 7l needs `manual.md` beside `repo/`; the next Route decides how.

## 052-route · 2026-10-15

Status: blocked-on-owner. Open: none.

After 7k (47): the test fix is built but the engineer did not run the suite. AC-15 needs the unchanged `manual.md` beside `repo/`, which no Role workspace has (29, 40, 47); another QA round would repeat the same missing input. Escalated to the Owner (48; A = Owner runs the suite, recommended; B = Owner places `manual.md` for QA). 7l is tentative on B.

## 054-resume · 2026-10-15

Status: active. Open: 49-studio-to-playtester.md.

After the Owner chose A (48, D-010): the suite ran 40/40 with the unchanged `manual.md`, so AC-15 passes. Goal back to `active`. 7l is skipped, and Play (8) opens as 49, a fresh Handoff composed from permitted information only. Review unchanged.

## 056-route · 2026-10-15

Status: active. Open: 51-studio-to-game-designer.md, 52-studio-to-playtester.md.

After Play (50): the report covers room 1 only (scripted, two defeats) and shows experience issues, not defects. Diagnose re-opens (9a, 51) per the Play return rule. A second Play (9b, 52, fresh playtester) opens in parallel for the unseen rooms. Review waits for both.

## 059-route · 2026-10-15

Status: active. Open: 55-studio-to-qa.md, 56-studio-to-game-designer.md, 57-studio-to-art-director.md.

After 9a/9b (53, 54): both done. The room 1–2 findings are tuning, rules and clarity within Option A, so no Decide now (D1/D2 held for a retest). 54 saw only room 2. Opened in parallel: QA fact checks and bots (10a), designer spec update (10b), art display (10c). Build, Verify, Play, Review follow.

## 064-route · 2026-10-16

Status: active. Open: 57-studio-to-art-director.md.

After 10a/10b (58, 59): both done; 10c (57) still open, so the Route waits for it. 59's rules already settle D-58-1 (a hit in Strike cancels it), dash distance, facing and miss wording. Left for Build/Verify: on-you knockback direction, "(miss)" first-hand, D-58-1 at 30 FPS. The Owner step for the manual draft (10-O) is now planned.

## 066-route · 2026-10-16

Status: active. Open: 61-studio-to-gameplay-engineer.md.

After 10c (60): done. The visual spec is text/display only, so no rule change and no escalation. Opened Build (12, 61) and Owner manual placement (10-O, 62) in parallel. 60's "Build updates manual.md" corrected to the D-005 pattern (Owner places). 13b confirmed planned (the view changes).

## 068-route · 2026-10-16

Status: active. Open: 64-studio-to-game-designer.md.

After Build 12 (63, question): Build could not start (no repo files in its packet) and the spec lacks the knockback direction at distance 0. Per the Build return rule, Design re-opens (12a, 64); Build re-issues as 12b with repo files named in Load. No parallel Build, since both touch the same files. No escalation.

## 070-route · 2026-10-16

Status: active. Open: 66-studio-to-gameplay-engineer.md.

After 12a (65): done. Q1 is settled by D-013 and AC-28; Q2 and three passages are clarified. No parameter, input or direction change, so no Decide and no escalation. Build re-issued as 12b (66) with the repo files in Load. 11 stays tentative.

## 072-route · 2026-10-16

Status: active. Open: 68-studio-to-qa.md, 69-studio-to-art-director.md.

After 12b (67): done, fits the plan; no spec gap, no escalation. Opened Verify in parallel: 13a QA (68, no Sender assessment, full suite with manual.md plus bots at 30/60 FPS) and 13b art-director (69). Tentative Plan (11) dropped: Waiting behavior is local.

## 075-route · 2026-10-16

Status: active. Open: 72-studio-to-game-designer.md.

After 13a/13b (70, 71): 13a failed (AC-17, AC-22 suite, AC-28b display at 30 FPS, V-10/14/16, V-15 manual); first failure of each, so no TD re-plan. Three spec gaps go to Design 13c (72) before Build. 13b was a question (AD could not run the build): not re-asked; visuals are reviewed after the rebuild from QA's captures. No escalation.

## 077-route · 2026-10-16

Status: active. Open: 74-studio-to-gameplay-engineer.md.

After 13c (73): done. The three spec gaps are ruled (D-014; AC-17, 28 changed, AC-29, 30 and V-18 new; V-10, 12, 14, 16 changed). No number, input or direction changes, so no Decide and no escalation. Build 13d opened (74), addressed back to `studio` so QA's step can be composed without the Sender assessment.

## 079-route · 2026-10-16

Status: active. Open: 76-studio-to-qa.md.

After 13d (75): done, fits the plan; no spec gap, no escalation. Verify 13f opened for `qa` (76), composed without the Sender assessment, both frame rates, with verbatim captures for the art-director. Owner step 13e-O (AC-15 with `manual.md`) runs in parallel, as the build environment lacked `manual.md`.

## 081-route · 2026-10-16

Status: active. Open: 78-studio-to-art-director.md.

After 13f (77): pass, no criterion failed, so no Build or TD re-plan. Opened 13g art-director (78) from QA's captures with the two QA observations, and re-asked the Owner for the AC-15 suite run and V-15 text (79). Designer clarification of AC-17 (Strike draws) stays optional, after 13g.

## 083-route · 2026-10-16

Status: active. Open: 82-studio-to-qa.md, 81-studio-to-playtester.md.

After 13g (80): pass for everything assessable; D-015 accepts lunge draws and the shot at spawn. No Build, no TD re-plan, no escalation. Opened in parallel: 14 Play (81, fresh playtester, build and profile only) and 13h QA captures for V-17 (82). 13i is tentative. Colour (V-6) is recorded as not checked.

## 086-route · 2026-10-16

Status: active. Open: 87-studio-to-art-director.md, 86-studio-to-playtester.md, 85-studio-to-game-designer.md.

After 13h (83): V-17 passes in both cases at 30 and 60 FPS; 13i opened (87) for the AD's reading and the dash-draw wording. After 14 (84): thin again (room 1 only, 3 defeats); its experience issues go to Diagnose 14c (85), and a fresh Play 14b (86) starts directly in rooms 3–5. No escalation.
