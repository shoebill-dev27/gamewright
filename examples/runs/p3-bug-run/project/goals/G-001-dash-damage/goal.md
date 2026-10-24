---
kind: goal
id: G-001
project: lantern-depths
status: done
created: 2026-10-11
---
# G-001: Player takes damage while dashing

## Owner request

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

## Interpretation

Success condition: when the player is in the state the game defines as "dashing" (and the design documents say the player should not be hurt then), no damage is taken. The Owner can no longer reproduce the case where a dashing player takes damage, at both 30 and 60 FPS.

Whether "dash should protect the player" is already specified (design/combat.md covers damage and invulnerability rules) was not read at Intake. The first step checked it: QA confirmed that combat.md specifies full invulnerability for the whole 0.25 s dash, so this is a defect.

Out of scope: changing the combat kit, adding input buttons (D-001), rebalancing damage or dash tuning beyond what the fix requires, and new enemies or rooms.

The Owner says the problem is reproducible but gave no steps. QA found a likely trigger (dashing shortly after being hit), but the enemy type, the part of the dash affected and any frame-rate dependence were unknown at the time. The root cause was for the `gameplay-engineer` to determine.

## Unknowns

Entry questions from development-loop.md:

- **Observe**: Done. QA reproduced the defect from the build description and wrote a defect report with acceptance criteria (01 → 02).
- **Diagnose**: Root cause is a defect-cause question owned by `gameplay-engineer`. It happens inside Build, so there is no separate stage.
- **Decide**: No real choice of direction arose. Dropped.
- **Design**: Skipped. QA confirmed that combat.md is unambiguous (dash = full invulnerability for 0.25 s).
- **Plan**: Dropped. The root cause was local to the player invulnerability logic and Verify passed on the first attempt.
- **Build**: Done.
- **Verify**: Done, pass.
- **Play / Review**: Skipped. This is a defect with a specified behavior, not an experience Goal, and no direction Decision is involved.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | 01-studio-to-qa.md (result: 02-qa-to-gameplay-engineer.md) |
| 2 | Design | game-designer | write-design-spec | skipped (combat.md already specifies full dash invulnerability) | — |
| 3 | Plan | technical-director | technical-plan | skipped (root cause local; Verify passed first time) | — |
| 4 | Build | gameplay-engineer | implement-change | done | 02-qa-to-gameplay-engineer.md (result: 03-gameplay-engineer-to-qa.md) |
| 5 | Verify | qa | verify-change | done | 03-gameplay-engineer-to-qa.md (result: 04-qa-to-studio.md, pass) |

Status: planned | tentative | open | done | skipped. Handoff: the file name (in this goal's directory)
of the incoming Handoff that starts the step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

Skipped: Decide, Diagnose (part of Build), Design (spec already unambiguous), Plan (not needed), Play and Review (defect, not an experience Goal).

## Route changes

- After step 1 (Observe): the outcome fits the plan. QA confirmed a defect against an unambiguous spec, which settles the tentative Design condition, so Design is now `skipped`. Plan stays tentative. The 02 handoff's stage was relabelled from Diagnose to Build, because diagnosis belongs to the engineer's Build step.
- After step 4 (Build): the outcome fits the plan. The engineer found a root cause local to the player invulnerability logic and had no open questions, so Plan stays tentative and Design stays skipped. Handoff 03 goes to `qa` directly. It was edited in place for QA's Independence: the root-cause explanation and the engineer's risk reasoning were removed from Findings (the Sender assessment stays on record and is stripped by the runtime), and the Load list now names `verify-change` and the post-fix build.
- After step 5 (Verify): the outcome fits the plan. QA passed every criterion at both 30 and 60 FPS with no open questions, and the original reproduction no longer produces damage during the dash. The tentative Plan condition (cross-system root cause, or the same criterion failing twice) did not occur, so Plan is `skipped`. There is no experience target and no direction Decision, so Play and Review stay skipped. The Goal is met and the Studio closes it.

## Next action

None. The Goal is closed; the Owner may review the Outcome below.

## Outcome

**結果**: G-001 は達成です。ダッシュ中にダメージを受ける不具合を修正しました。

- 原因の切り分け: QA が、被弾直後にダッシュするとダッシュ中でもダメージを受ける、という再現条件を特定しました。`design/combat.md` ではダッシュは 0.25 秒間完全無敵と明記されているため、仕様どおりでない不具合と判断しました。
- 修正: ゲームプレイエンジニアがプレイヤーの無敵判定ロジックを修正しました（ビルド 0.4）。入力ボタンの追加はありません（D-001 を順守）。
- 検証: QA が受け入れ基準を 30 FPS と 60 FPS の両方で確認し、すべて合格しました。被弾後 0.3〜0.79 秒でのダッシュ、Grub との接触、Spitter の弾、被弾なしのダッシュのいずれでも、ダッシュ中のダメージは発生しません。ダッシュの移動距離（4 タイル／0.25 秒）、クールダウン（0.6 秒）、攻撃の先行入力、被弾後の無敵（被弾から 0.8 秒後まで）も仕様どおりです。元の再現手順でも症状は出なくなりました。

**記録した Decision**: なし（既存の仕様と D-001 の範囲内で完結）。

**次の課題（新しい Goal の提案）**:
- ビルド 0.4 では、被弾直後に以前より少し安全に感じられる可能性があります。早めにダッシュしても被弾後の無敵が 0.8 秒まで保たれるためで、仕様どおりの挙動です。気になる場合は、`game-designer` による調整を別の Goal として検討してください。

**オーナーへの確認事項・注意点**:
- 今回は実ビルドがないドライランのため、30 FPS と 60 FPS の結果は、ビルド説明（`sim/build-0.4.md`）が両方で同じ結果になると述べていることに基づきます。フレームレートごとの個別の記録やログはありません。
- ご自身の環境で元の再現手順を試して、症状が出ないことを確認していただけると確実です。
