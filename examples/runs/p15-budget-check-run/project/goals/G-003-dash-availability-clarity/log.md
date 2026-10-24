# Goal log

One entry per Intake, Route and Resume, appended by whoever runs the operation.
Entries are never edited.

## 001-intake · 2026-10-23

Status: active. Open: 01-studio-to-game-designer.md.

Intake: initial route. Observe and Plan are skipped (reasons under Unknowns); Decide is tentative.

## 003-route · 2026-10-23

Status: active. Open: 03-studio-to-game-designer.md.

After Diagnose (02): the cause is missing display information, and no option touches dash rules, inputs or scope. Decide is therefore skipped, and Design opens with options A+B+C. Observe and Plan stay skipped.

## 005-route · 2026-10-23

Status: active. Open: 05-studio-to-gameplay-engineer.md.

After Design (04): the spec is complete and touches no dash rules, inputs or scope, so no Decide or Plan. D-028 rebases only G-002's stopped L1 criterion, so no escalation. Build opens; Q3–Q5 are left to observation in Build and Verify.

## 007-route · 2026-10-23

Status: active. Open: 07-studio-to-gameplay-engineer.md.

After Build (06, partial): the engineer lacked the source files, and the spec is fine. Build goes back to the same Role with `game.py`, `run_driver.py`, `session.py` and the tests in the Load list. No stage added and no QA yet, because nothing was built.

## 009-route · 2026-10-23

Status: active. Open: 09-studio-to-qa.md.

After Build (08, done; Build check 173 tests OK): the result fits the plan, so Verify follows with no added stage. The QA Handoff omits the Sender assessment and asks QA to judge the public-driver picture difference and Q3–Q5, Q7, Q8 by observation.

## 011-route · 2026-10-23

Status: active. Open: 11-studio-to-game-designer.md.

After Verify (10, fail): the failures come from an ambiguous spec, not a build defect, so the return rule sends it to Design, not Build. Design is reopened for the 30 FPS tolerance, public-driver pictures, rule-driven refusals and the Q8/Q12 evidence. Build and re-Verify are tentative, and Play is held until the rulings are in.

## 013-route · 2026-10-23

Status: active. Open: 13-studio-to-gameplay-engineer.md.

After Design (12, done): the rulings fit the plan. Only a small Build is needed (legacy rule-driven refusal print, manual text). No timing change, so no Decide or Plan. Verify and Play become parallel after Build. Budget will run out before Review; a scope cut may be needed.

## 015-route · 2026-10-23

Status: active. Open: 15-studio-to-qa.md, 16-studio-to-playtester.md.

After Build (14, partial): the legacy rule path now prints the refusal with no game change. Nothing else is missing for the Role, and the before/after comparison cannot be made, so QA does an after-only check and lists it as unverifiable. QA (15) and a fresh Playtester (16) open in parallel. The budget runs out after them.

## 018-route · 2026-10-23

Status: active. Open: 19-studio-to-game-director.md.

After Verify (17) and Play (18): no failure, but QA left items unverified, found one spec gap, and the Playtester raised hit-stun display and `(nothing happens)`. The budget is used, so Design, Build and QA are not opened. The Review opens as a `game-director` step that also cuts remaining work or escalates the cost.

## 020-route · 2026-10-23

Status: done. Open: none.

After Review (20, goal-met): the Goal is Closed. Unobserved verification items are `skipped` under the D-030 scope cut. Hit-stun reason display, `(nothing happens)`, grub warning countdowns and optional verification become proposed Goals. No Owner cost escalation was needed.
