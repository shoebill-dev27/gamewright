# Goal log

One entry per Intake, Route and Resume, appended by whoever runs the operation.
Entries are never edited.

## 001-intake · 2026-10-16

Status: active. Open: 01-studio-to-playtester.md.

Initial route from Intake (pattern: experience problem, cause unknown). No changes yet.

## 003-route · 2026-10-16

Status: active. Open: 03-studio-to-game-designer.md.

After step 1 (Observe): the outcome fits the plan, so Diagnose follows. The report is thin (scripted play, rooms 4–5 unseen); the Diagnose Handoff lets the designer check with bots/trace and say if more observation is needed. No stage added or dropped.

## 005-route · 2026-10-16

Status: active. Open: 05-studio-to-game-designer.md, 06-studio-to-qa.md.

After step 2 (Diagnose): fits the plan. Decide is skipped (no real choice, no trigger). Added a parallel QA Observe for the 30/60 FPS bot divergence, since Design's criteria depend on both rates. A separate rooms 4–5 playtest is not added; the final Play covers it.

## 008-route · 2026-10-16

Status: active. Open: 09-studio-to-gameplay-engineer.md.

After steps 4a and 4b: both fit the plan. Plan is skipped (designer: no cross-system approach). QA found no build defect, so the bot fix is added to Build instead of a separate step. The art-director visual review is now planned.

## 010-route · 2026-10-16

Status: active. Open: 11-studio-to-game-designer.md, 12-studio-to-art-director.md, 13-studio-to-qa.md.

After step 6 (Build): partly fits. Criteria 1–12 and 15 look met per the engineer; 14 missed, five spec gaps used defaults, walker 30/60 divergence open. Added 7a Design (designer), 7c QA divergence check, and 7b art-director cue review in parallel. Full QA Verify waits so it runs against final criteria.

## 014-route · 2026-10-16

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After 7a–7c: the designer ruled 14 and 16 with no build or bot change; the art review concerns a future graphical build only; QA found no build defect, but 16e is unproven (the log lacks positions). Added 7d Build (logging only, test aligned with the ruling) before Verify, and tentative 8b Design for a frame-rate graze.

## 016-route · 2026-10-16

Status: active. Open: 19-studio-to-qa.md.

After 7d: the engineer reports log-only changes with byte-identical log-off output, so the plan holds. Opened Verify (QA, criteria 1–16 + V12, incl. 16e from the new log) with a Handoff that omits the engineer's assessment. 8b stays tentative on the 16e result.

## 018-route · 2026-10-16

Status: active. Open: 21-studio-to-game-designer.md.

After 8 (Verify): partly fits. 1–15 and 16a–d pass; the walker difference is bot timing. QA found a frame-rate-dependent graze plus a cap and margin question, which only the designer can rule. 8b is now open (handoff 21). Added 8c Build (tentative) and 8d Verify (planned).

## 021-route · 2026-10-16

Status: active. Open: 23-studio-to-qa.md.

After 8b (Design): fits. The designer accepted the graze (D-002), ruled the cap is on cue starts, kept the walker margin and named the governing documents; the build does not change. 8c is skipped. 8d (QA) is open (handoff 23, no designer assessment) to run the 30 FPS gaps and criterion 17.

## 023-route · 2026-10-16

Status: active. Open: 25-studio-to-playtester.md, 26-studio-to-game-designer.md.

After 8d (Verify): fits. QA passed criteria 1–17 at 30 and 60 FPS; only V12 stays open (no graphical build). Opened 9a Play (fresh playtester, build and player profile only) and, in parallel, 9b Design for two non-blocking QA notes on the contact edge (wording and D-002 record).

## 027-route · 2026-10-16

Status: active. Open: 26-studio-to-game-designer.md, 28-studio-to-game-designer.md, 29-studio-to-qa.md.

After 9a (Play): does not fit "goal met". The playtest reports remaining monotony (melee enemies share one answer, dash unused, spitter crossfire) and one possible defect. Returned to Diagnose (10a, designer) and Observe (10b, qa) in parallel with open 9b. Decide, Design, Build, Verify and Play are tentative on the Diagnose result.

## 031-route · 2026-10-16

Status: active. Open: 33-studio-to-game-designer.md, 34-studio-to-qa.md.

After 9b, 10a, 10b: all fit. Diagnose 31 needs no Decide (options inside D-001), so Decide stays tentative. Room 2 hit is not a defect (32). Opened Design (33, Options 1–2, manual wording) and, in parallel, a QA spitter-timing trace (34) to settle the "in sync" conflict. Build, Verify, Play are now planned.

## 034-route · 2026-10-16

Status: active. Open: 37-studio-to-game-designer.md.

After 12a and 12b: both fit. Design 35 is complete (no Decide). QA 36 found no defect in 0.5 but an undefined rule (shot touching an invulnerable player) and room 3 cue overlap. Added 12c Design (37) before Build so contact code changes once.

## 037-route · 2026-10-16

Status: active. Open: 39-studio-to-gameplay-engineer.md.

After 12c (Design 38): fits. The designer ruled on blocked contact (D-005: shot consumed, lunge spent) and accepted simultaneous cue starts outside rooms 4–5; the spec is complete and no direction or scope change arose, so Decide stays tentative. Opened Build 0.6 (39) with the full change list; its result is addressed to `studio` for an independent Verify.

## 039-route · 2026-10-16

Status: active. Open: 41-studio-to-qa.md, 42-studio-to-game-designer.md.

After 13 (Build 0.6, 40): fits; the engineer found no spec gap. One bot figure (walker, 60 FPS, rooms 3–5: 7 hearts vs limit 6) is a tuning question, so Design (42) runs in parallel with independent Verify (41). Build was not rerouted; the Sender assessment was not passed to QA.

## 042-route · 2026-10-16

Status: active. Open: 45-studio-to-game-designer.md.

After 14a/14b: Verify 0.6 failed (43): F2 (brute shrug message missing in player view) and F3 (banner 0.5) are defects. Criterion 13 at 60 FPS is settled by Design 44 (D-006). Room 3 cap vs criterion 11 goes to Design (45) before Build so enemy code changes once; then Build, full re-verify, Play.

## 044-route · 2026-10-16

Status: active. Open: 47-studio-to-gameplay-engineer.md.

After 15 (Design 46): fits. Room 3 cap accepted as built (D-007), criterion 11 reworded; no enemy change, D-004/D-005/D-006 unchanged, no Decide. Build 16 is narrowed to F2 and F3 only (47), result addressed to `studio`; QA re-verify adds criterion 11 a–e.

## 046-route · 2026-10-16

Status: active. Open: 49-studio-to-qa.md.

After 16 (Build 0.6.1, 48): fits. F2 and F3 fixed in `play.py` only; the engineer ran no tests, so QA must run the suite first. Opened Verify 17 (49), a fresh Handoff without the implementation history or Sender assessment, covering the "not run" list, criterion 11 a–e and criterion 13 per D-006.

## 048-route · 2026-10-16

Status: active. Open: 51-studio-to-playtester.md, 52-studio-to-game-designer.md.

After 17 (Verify, 50): pass at 30 and 60 FPS; F1–F3 fixed, no repeated failure. Unrun items left to the playtest. Opened Play 18a (51, fresh, no change or expected result) and, in parallel, a small Design step 18b (52) for the criterion 11d wording.

## 052-route · 2026-10-16

Status: active. Open: 55-studio-to-qa.md.

After 18a/18b (53, 54): 11d reworded, no build change. The playtest reports unfair-feeling swipe/lunge hits and one uncued hit, so QA Observe 18c (55) comes before Review. "Rooms feel alike" would be a third Diagnose pass, so it goes to `game-director` Review with the playtest and the QA result.

## 054-route · 2026-10-16

Status: active. Open: 58-studio-to-game-designer.md, 57-studio-to-game-director.md.

After 18c (56): not a defect; the late-swipe hits and the "no cue" hit match the design (a cue was printed). Opened Review (57) with playtest 53 and QA 56, since "rooms feel alike" would be a third Diagnose pass. In parallel, non-blocking Design 18d (58): manual wording on late swipes and the per-variant cue message.

## 057-route · 2026-10-16

Status: active. Open: 61-studio-to-playtester.md, 62-studio-to-qa.md.

After 18d and 19 (59, 60): Review is goal-not-met; per D-009 the next pass is a variant-aware playtest, not a third Diagnose. Opened Play 20a (61, build 0.6.1 unchanged) and QA 20b (62, 30 FPS gaps) in parallel. Manual text (59) and the D-008 message change wait until after the playtest so the played build stays steady.

## 060-route · 2026-10-16

Status: active. Open: 65-studio-to-game-director.md, 66-studio-to-game-designer.md.

After 20a and 20b (63, 64): playtest shows rooms 4–5 varied, room 3 and brute loop repetitive, brute/runner messages read "a grub". QA closed the 30 FPS gaps with no defect. Opened Review pass 2 (65) and, in parallel, a non-blocking Design check (66: room 3 in-flight vs D-007; D-008 readiness). Build waits for both.

## 063-route · 2026-10-16

Status: active. Open: 69-studio-to-gameplay-engineer.md, 70-studio-to-game-designer.md.

After 21a/21b (67, 68): Review pass 2 is goal-not-met with a narrow gap and no Owner escalation (D-010). Design kept D-007 for room 3 in-flight and accepted D-011 (variant-named messages). Opened Build 22a (69: D-011, manual text) and, in parallel, Design 22b (70: room 3 variety). A room 3 Build follows only if 22b specifies one; then Verify, fresh playtest, Review pass 3.
