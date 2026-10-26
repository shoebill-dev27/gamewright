---
kind: decision
id: D-006
status: accepted
decided_by: game-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-006: close G-002 on partial evidence; unseen scenes go to the Owner as look-and-confirm; the dim change becomes a follow-up

## Decision

1. **No more Build, Verify or Play steps in G-002.** The budget is 13 and 16 are used. Further verification would need a tool change (`shot` with a URL hash or viewport, or a QA fixture page). Neither can be made inside the Goal's means, and a run without that change would only repeat the quiet start frame.
2. **The Goal is closed as "built, not fully verified".** Facts that stand:
   - 69 of 69 tests pass, including the golden hashes and the criterion 45 test, which compares page marks with text marks over scripted runs with a hound crouch and a Gloom gather.
   - The page loads with no console errors.
   - Seen and fine on the page: wall, floor, unlit brazier, player, `<`, moth at a distance, remembered versus visible wall, and the ember flame at r = 6.
   - Nothing seen fails any criterion.
   - **Not seen by anyone**, so not claimed:
     - threat marks and the D-005 `!` chip
     - reach marks and letter backing (the criterion 44 re-check is still open)
     - hound, shade and Gloom
     - stunned creatures
     - the flame at r = 2
     - items in slots
     - the lit brazier
     - the 1280 px layout, which is computed at about 1130 to 1190 px and not measured
3. **The Owner looks and confirms at Close.** The Close handoff, in Japanese, carries the list in the attached handoff (17). If the Owner sees a failure, it becomes a new Goal. The marks carry pillar 1, so a mark failure is the first thing to fix.
4. **The `dim()` factor change (0.55 to 0.65) is not built in this Goal.** It is a taste adjustment to remembered floor. It fails no criterion, and a Build now would be one more unverified change on top of unverified scenes. It is listed as a proposed follow-up, with 0.60 as the fallback. The Owner may ask for it after looking.
5. **Route.**
   - Step 8, Play: `skipped`. The page cannot be shown to a playtester with the available means. Say this at Close.
   - Review: stays `skipped`.
   - The next step is Close, with the Owner look-and-confirm list.

Limits: this changes no rule, no mark, no earlier Decision and no part of the Goal's meaning. It does not declare any unseen criterion passed. Criteria 32, 33, 35 (on `<` and a lit brazier), 36 (r = 2), 37, 40, 42 to 44 and 46 stay "not verified". Only criteria 34 and 41 passed on the frames seen, and 38, 39, 47 and 48 passed only in part or for limited scenes.

## Rationale

- The Owner's request is "put a picture on each of them". That is built, and the part seen matches the cave-and-ember mood.
- The remaining risk is in the marks, and the Owner can check that by opening the page. No step the Studio has is able to check it.
- Escalating the cost would ask the Owner for budget, or for a tool change, to verify what the Owner can see directly. Looking is cheaper and gives better evidence than another QA pass.
- Mark equality between page and text is covered by an automated test. That lowers, but does not remove, the risk that a picture hides a mark.

## Alternatives considered

- **Hold the Goal until the marks are seen (Art Director's recommendation).** Right in principle, but it needs a tool change the Studio cannot make. The Owner look-and-confirm gives the same hold, with the Owner as the viewer, and costs no budget.
- **Escalate extra budget or a `shot` extension.** A cost question with a cheaper answer. Kept as the fallback if the Owner prefers the Studio to verify.
- **One more Build for `dim()` now.** Dropped, see point 4.

## Revisit when

The Owner reports a hidden or unreadable mark, a missing picture, a layout problem at their screen width, or wants the dim change. Then open a new Goal. If the `shot` tool later gains a hash or viewport option, a verification pass becomes cheap.
