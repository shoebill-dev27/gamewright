---
kind: goal
id: G-001
project: lantern-depths
status: done
created: 2026-10-10
---
# G-001: Player takes damage while dashing

## Owner request

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

## Interpretation

The Owner reports a defect: the player sometimes takes damage while in the middle of a dash. The Owner says it is reproducible and wants it fixed.

Success condition (qualitative): when the player is dashing, damage is applied exactly as the combat design says it should be during a dash. The situations the Owner saw, where damage landed mid-dash, no longer happen, and nothing else about dash or damage regresses. It must hold at both 30 and 60 FPS, a project constraint.

Numeric thresholds, such as invulnerability frame counts, belong to the design's acceptance criteria. They are not set here.

Out of scope:
- Changing the dash or damage rules as a design improvement.
- Adding buttons or inputs (D-001).
- Rebalancing enemies.
- Any experience or feel tuning.

Note for the route: the Owner assumes dash should prevent damage. QA has since confirmed that `design/combat.md` states this (the player is invulnerable for the full dash duration).

## Unknowns

Entry questions from `development-loop.md`:

- **Observe: has the problem been reproduced first-hand?** Done. QA reproduced it on the dry-run build description: damage partway through a dash started shortly after taking a hit (intermittent). Defect report in `02-qa-to-gameplay-engineer.md`.
- **Diagnose: is the cause understood?** For defects, root cause belongs to `gameplay-engineer` as part of Build (Decision authority), so there is no separate Diagnose stage. The engineer identified a cause (see 03).
- **Decide: is there a real choice of direction, priority or scope?** No. Nothing conflicts with the vision or with D-001, so the stage is skipped.
- **Design: is the intended behavior specified well enough to build and verify?** Yes. `design/combat.md` specifies full-duration dash invulnerability with no exception. The one gap surfaced in Verify (criterion 6, tolerance for a one-frame difference at a protection-expiry boundary) was ruled by the Game Designer in step 6 (D-002).
- **Plan: is the technical approach non-obvious, risky, cross-system or parallelizable?** No. The engineer reports a local fix in the player's shared invulnerability logic. Skipped.
- **Build:** done. It did not reopen, because the final Verify passed.
- **Verify:** always after Build. Criteria 1–5 passed in step 5, and criterion 6 passed under D-002 in step 7. Overall verdict: pass.
- **Play / Review: skipped.** The Goal is a defect, not about feel, and involves no direction Decision.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | [01-studio-to-qa.md](01-studio-to-qa.md); result: [02-qa-to-gameplay-engineer.md](02-qa-to-gameplay-engineer.md) |
| 2 | Design | game-designer | write-design-spec | skipped (intended behavior is defined in `design/combat.md`; the criterion 6 gap is handled in step 6) | — |
| 3 | Plan | technical-director | technical-plan | skipped (the engineer reports a local fix; see Route changes) | — |
| 4 | Build | gameplay-engineer | implement-change | done | [02-qa-to-gameplay-engineer.md](02-qa-to-gameplay-engineer.md); result: [03-gameplay-engineer-to-qa.md](03-gameplay-engineer-to-qa.md) |
| 5 | Verify | qa | verify-change | done (no overall verdict: criteria 1–5 pass, criterion 6 undecided; returned as `question`) | [05-studio-to-qa.md](05-studio-to-qa.md); result: [06-qa-to-studio.md](06-qa-to-studio.md) |
| 6 | Design (criterion 6 tolerance) | game-designer | write-design-spec | done (ruling: expiry may be late by under one frame, never early; D-002) | [07-studio-to-game-designer.md](07-studio-to-game-designer.md); result: [08-game-designer-to-studio.md](08-game-designer-to-studio.md) |
| 7 | Verify (final verdict) | qa | verify-change | done (pass: criteria 1–6 at 30 and 60 FPS, no regressions) | [09-studio-to-qa.md](09-studio-to-qa.md); result: [10-qa-to-studio.md](10-qa-to-studio.md) |
| 8 | Build | gameplay-engineer | implement-change | skipped (the ruling accepts the edge-timing difference; step 7 passed, so it never reopened) | — |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

- After step 1 (Observe): Design dropped (skipped). QA confirmed the expected behavior is specified in `design/combat.md`, and the build contradicts it in one reproduced case. Plan stays tentative, since the cause is not yet known.
- After step 4 (Build): Plan dropped (skipped). The engineer's condition for Plan (a non-local cause) did not occur: the cause is in the player's shared invulnerability logic and frame rate only shifts the boundary by up to one frame. Verify follows as planned. The Handoff to QA was edited in place: the Sender assessment and the root-cause reasoning were removed (QA policy), the Load list now points at `sim/build-0.4.md`, and the verdict is to be addressed to `studio`.
- Caveat for the record: the engineer reported that it had no way to run or edit source in its operation and has no test results. The fix is untested. QA should report a blocker if the build under test does not show the changed behavior. A blocker or a failure goes back to `gameplay-engineer`.
- After the first Verify attempt (04, outcome `question`): no verdict was issued. QA blocked because `sim/build-0.4.md` is a description, not a runnable build. The Studio resolved this from the Project Context: `project.md` defines this as a dry-run sample project with no repository, where builds are simulated under `sim/` and "running the build" means reading the `sim/build-*.md` file, which is the project's `player_visible` artifact. The description is therefore the build under test. This is a process ruling, not a design or verdict ruling. Verify was re-routed to QA (05). No failure was recorded, so the second-failure loop limit is not triggered.
- After the second Verify attempt (06, outcome `question`): criteria 1–5 pass at 30 and 60 FPS, and the original reproduction no longer shows damage. Criterion 6 is undecided. Return rule "Verify: the expected behavior is undefined" applies, so the route went to Design (`game-designer`, step 6) with that question only. Step 7 (Verify, final verdict) was added after it. Step 8 (Build) was tentative.
- Escalation check for 06: no trigger fires. A frame-rate tolerance for protection expiry is a rule/tuning question inside `game-designer` authority.
- After step 6 (Design, 08, outcome `done`): the Game Designer ruled that protection expiry may be late by under one frame at the running frame rate and must never be early, for both boundaries and both enemy types, and recorded D-002. This accepts the edge-timing difference, so the tentative step 8 (Build) is dropped (skipped). Escalation check: no trigger fires. No dash or damage rule changed, the vision and D-001 are untouched, and no direction or scope change is implied.
- Handoff 09 to QA was composed by the Studio from the criteria and the ruling only. It leaves out the designer's statement of the expected verdict, so that QA verifies from the spec and the build (QA Independence), and it asks for the result to be addressed to `studio`.
- After step 7 (Verify, 10, outcome `pass`): criteria 1–6 pass at 30 and 60 FPS and no regression was found. The loop limits are not triggered (no criterion failed). Escalation check: no trigger fires. 10 suggests routing to Review, but Play and Review were skipped at Intake and still apply: the Goal is a defect, not an experience Goal, and no direction Decision was involved (D-002 is a rule-level ruling by `game-designer`). Per the development loop, a defect needs no Play or Review, so the Goal goes straight to Close. QA's optional wording note on the exact-instant boundary is recorded as a proposed follow-up, not as scope growth.

## Next action

None. The Goal is closed. The Owner may decide on the proposed follow-ups in the Outcome.

## Outcome

結果:
- 「ダッシュ中にダメージを受ける」不具合は、被弾直後（入力が戻る約0.3秒後）にダッシュした場合に、ダッシュ途中で無敵が切れて被弾する、という再現可能な形でQAが再現を確認しました。
- 修正（ビルド0.4）の後、QAが最終検証を行い、全6基準が30FPSと60FPSの両方で合格しました。被弾直後のダッシュではGrubの接触でもSpitterの弾でもダメージを受けません。被弾後0.8秒の無敵が途中で切れることもありません。
- 退行はありません。通常の被弾（1ハート、0.3秒の硬直、0.8秒まで無敵）、被弾なしのダッシュ、ダッシュの距離（4タイル／0.25秒）、クールダウン0.6秒、ダッシュ中に押した攻撃がダッシュ終了時に出る挙動は、すべて従来どおりです。D-001（入力は攻撃とダッシュのみ）にも影響していません。

行った判断（Decision）:
- D-002（ゲームデザイナー）: 無敵の終了判定は、実行中のフレームレートで最大1フレーム未満だけ遅れてもよいが、早く切れてはならない。ダッシュ終了時と被弾後0.8秒の両方の境界、両方の敵タイプに適用。ダッシュやダメージのルール自体は変更していません。`design/combat.md` にも記載済みです。

次の課題（提案。新しいGoalとして扱い、今回の範囲には含めていません）:
- 終了時刻ちょうどの接触を「保護される」と明文化するかどうか（QAの任意の指摘。デザイン文言の明確化のみで、判定には影響しません）。
- 今回のビルドは試験用の記述（`sim/build-0.4.md`）であり、実機での実行・テストは行われていません。実際のリポジトリがあるプロジェクトに移行する際は、実ビルドで同じ基準を再検証することを推奨します。

オーナー確認が必要な項目: なし。
