---
kind: handoff
goal: G-001
seq: 22
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 22: studio → gameplay-engineer — confirm the placed `manual.md` with `run_tests`

## Task

The Owner has placed the draft `manual.md` at the project root, unchanged. Run `run_tests` (`python3 -m unittest discover -s tests` in `repo/`) and report whether all 34 tests pass, including `ManualTest`. Do not write `manual.md`.

## Context

Goal G-001 (combat feels monotonous). Build 0.5 code (T1–T7, T9) was finished in step 18, with 33/34 tests passing. The only open item, T8 `manual.md`, was blocked twice on write access (18, 20) and escalated to the Owner (21). The Owner chose Option A (D-005): the Draft `manual.md` from 18 was placed verbatim at the project root. `ManualTest` reads `REPO.parent / "manual.md"`. The next steps are Verify (`qa` and `art-director`, in parallel), then Play and Review.

## Findings

- The Owner's response and the choice are in `21-studio-to-owner.md` and D-005.
- The Draft `manual.md` text is in `18-gameplay-engineer-to-studio.md` under "Draft `manual.md`". The engineer's earlier reading found it consistent with the implementation, but it was never tested.
- `run_tests` was 33/34 before the manual was placed. The one failure was `ManualTest`.

## Decisions already made

- D-001: one attack button plus dash; no new buttons.
- D-002: Option A, rework existing enemy behavior first.
- D-003: room mix, zero hearts ends the run, room clear heals one heart.
- D-004: Option A as one sequential change set (item 5: the manual belongs to the gameplay-engineer).
- D-005: the Owner placed the draft `manual.md` unchanged (Option A of Escalation 21).

## Constraints

- Run only `run_tests`. Do not edit code, tests or `manual.md` unless the failure is in code you own and the fix is within spec AC-1…AC-17 and V-1…V-8 and the plan. The write access to `manual.md` was not granted (D-005 is a one-time placement).
- If `ManualTest` fails because of the text of the placed `manual.md`, do not edit it. Report the exact failing assertion, the line in `manual.md` it concerns, and the suggested corrected text, with outcome `question`, so the Studio can ask the Owner again. This would be a new input, not a repeat of the earlier block.
- If a different test fails, diagnose and fix it within your authority, or hand back per your contract if the spec is ambiguous.
- Must play correctly at 30 and 60 FPS (project constraints).

## Open questions

None.

## Expected output

A short build note in Findings of your outgoing Handoff: the test command, the result (pass/fail count, names of any failures) and any change you made, with a sha or file list if you changed anything. Address the result to `studio` (not to qa), because the Studio composes QA's fresh Handoff without the Sender assessment. Use `outcome: done` if 34/34 pass, otherwise `question` or `fail` as appropriate.

## Sender assessment

The Studio did not read the draft. The risk is small: the earlier reading found no contradiction and the Owner placed the text unchanged. Pause (F11) is not implemented; this is known and QA marks it not verifiable.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, manual.md, design/combat.md, design/combat-visuals.md, repo/README.md, repo/game.py, repo/tests/test_game.py, goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md, goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
- Decisions: decisions/D-004-option-a-single-change-set.md, decisions/D-005-owner-places-manual-draft.md
- Previous handoff: goals/G-001-combat-monotony/21-studio-to-owner.md
