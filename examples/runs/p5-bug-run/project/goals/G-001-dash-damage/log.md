# Goal log

One entry per Intake, Route and Resume, appended by whoever runs the operation.
Entries are never edited.

## 001-intake · 2026-10-13

Status: active. Open: 01-studio-to-qa.md.

Intake: initial route. Pattern "reproducible defect": Observe → Build → Verify. Design, Decide and Plan are tentative, with their trigger conditions listed under Unknowns.

## 003-route · 2026-10-13

Status: active. Open: 02-qa-to-gameplay-engineer.md.

After Observe: QA reproduced the defect (damage on the last dash frame, both frame rates) and `design/combat.md` defines the intended behavior. Design and Decide are dropped as skipped; Plan stays tentative. Build is next; the engineer addresses the result to `studio` so Verify gets a fresh Handoff.

## 005-route · 2026-10-13

Status: active. Open: 04-studio-to-qa.md.

After Build: the engineer delivered the fix and regression tests without needing a Plan, so Plan is skipped. Verify is open with a fresh Handoff (04) for QA that omits the engineer's Sender assessment. If Verify passes, the Goal closes.

## 007-route · 2026-10-13

Status: done. Open: none.

After Verify: QA passed every acceptance criterion at 30 and 60 FPS with no regressions (05). No stage is tentative or open, no escalation trigger fires, so the Goal is closed. The projectile-contact grace question is proposed as a possible new Goal, not added to scope.
