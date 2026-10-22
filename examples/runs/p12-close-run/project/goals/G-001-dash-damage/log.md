# Goal log

One entry per Intake, Route and Resume, appended by whoever runs the operation.
Entries are never edited.

## 001-intake · 2026-10-23

Status: active. Open: 01-studio-to-qa.md.

Intake: initial route (pattern 1, reproducible defect), with Design and Plan tentative.

## 005-route · 2026-10-23

Status: active. Open: 02-qa-to-gameplay-engineer.md.

After Observe: defect reproduced (deterministic, FPS-independent) and combat.md defines the intended behavior, so Design is skipped. Plan stays tentative. Build is open with the QA defect report.

## 007-route · 2026-10-23

Status: active. Open: 04-studio-to-gameplay-engineer.md.

After Build (03): the runtime's test run failed (1 of 10, the new dash test at 30 FPS, hearts 1 != 2), so the build is not sent to QA. Routed back to the engineer with the failure to resolve and run the suite; Verify follows once green.

## 009-route · 2026-10-23

Status: active. Open: 05-gameplay-engineer-to-qa.md.

After Build (05): the test failure was a test artifact and the suite is now green, so the plan holds. Verify is open. The Handoff was trimmed in place to criteria and ways to exercise the build, without the engineer's reasoning or results, so QA verifies independently.

## 011-route · 2026-10-23

Status: done. Open: none.

After Verify (06): pass on all criteria. The dash-end-frame gap is non-blocking and not the reported defect, so no Design step is added; it becomes a proposed new Goal rather than scope growth. Goal closed.
