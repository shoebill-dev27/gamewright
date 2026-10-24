---
kind: goal
id: G-001
project: lantern-depths
status: done
created: 2026-10-13
---
# G-001: Player takes damage while dashing

## Owner request

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

## Interpretation

Success condition: in the build, the player no longer takes damage at moments when the game's rules say the player is dashing (and therefore protected). The Owner reports it is reproducible, but gave no steps. Whether "dashing" means invulnerable for the whole dash or only part of it is to be confirmed against `design/combat.md` (damage and invulnerability rules), not assumed here.

Out of scope: changing the dash design (distance, cooldown, invulnerability length) unless the design documents turn out to be silent or contradictory; new input buttons (D-001); other combat tuning.

Context check: the vision (one-button combat, readable threats) and D-001 are not in conflict with this fix. No immediate escalation. The constraint "must play correctly at both 30 and 60 FPS" is relevant: the defect may depend on frame rate, so reproduction should check both.

## Unknowns

- Observe: settled. QA reproduced the defect at 30 and 60 FPS (damage on the last dash frame); see 02-qa-to-gameplay-engineer.md.
- Diagnose: skipped as a separate stage. Root cause of a defect belongs to `gameplay-engineer` during Build.
- Design: skipped. `design/combat.md` states the dash is invulnerable for the full duration, so the intended behavior is defined.
- Decide: skipped. The fix does not change the dash's design intent or scope.
- Plan: skipped. The engineer built the fix without needing a plan or handing back.
- Build: settled. Fix and regression tests delivered (03-gameplay-engineer-to-studio.md).
- Verify: settled. QA passed all criteria at 30 and 60 FPS on build 36b3b8f9a16e, no regressions (05-qa-to-studio.md).
- Play and Review: skipped. This is a defect, not an experience Goal, and no direction Decision was involved.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | 02-qa-to-gameplay-engineer.md |
| 2 | Design | game-designer | write-design-spec | skipped | — |
| 3 | Decide | game-director | make-decision | skipped | — |
| 4 | Plan | technical-director | technical-plan | skipped | — |
| 5 | Build | gameplay-engineer | implement-change | done | 03-gameplay-engineer-to-studio.md |
| 6 | Verify | qa | verify-change | done | 04-studio-to-qa.md (result: 05-qa-to-studio.md) |

Status: planned | tentative | open | done | skipped. Tentative conditions are in Unknowns.

## Route changes

After Verify: QA passed every acceptance criterion at 30 and 60 FPS with no regressions (05). No stage is tentative or open, no escalation trigger fires, so the Goal is closed. The projectile-contact grace question is proposed as a possible new Goal, not added to scope.

## Next action

None. Goal closed. Owner may decide whether to start the proposed follow-up Goal (see Outcome).

## Outcome

結果:
- 不具合を修正し、QAが独立して検証して合格しました(ビルド sha 36b3b8f9a16e)。
- 原因: ダッシュ最終フレームでダメージが入っていました(30FPS・60FPSの両方で再現)。`design/combat.md` の「ダッシュ時間中は完全に無敵」という仕様どおり、ダッシュ終了フレームまで被弾しなくなりました。
- 検証内容: 再現スクリプト(30/60FPS)、すり抜け、Spitterの弾(ダッシュ最初・最後のフレーム)、上下左右のダッシュ、部屋1〜5、ダッシュ中に被弾後タイマーが切れるケース、先行入力の攻撃を確認。テストは7件から14件に増え、すべて成功しました。
- 回帰: なし。Grubの噛みつき(1ハート、0.8秒間隔)、ダッシュ距離(4マス)、クールダウン、Spitterの発射間隔は従来どおりです。

決定(Decision):
- 新規のDecisionはありません。ダッシュの設計意図は変えず、新しい入力ボタンも追加していません(D-001に適合)。

次の課題(新規Goal案):
- ダッシュ終了直後の1フレームで、重なっているGrubや弾が次フレームにダメージを与えます。これはGrubについては合意済みの挙動で、`design/combat.md` は弾の扱いについて何も定めていません。ダッシュ後の猶予時間を設けるかは設計変更になるため、今回の範囲外です。

Owner確認事項:
- 上記の「ダッシュ終了直後の猶予」を検討したい場合のみ、新Goalとして指示してください。不要であれば対応は要りません。
- 補足: 実際のSpitterスクリプトでは、弾が最終フレームちょうどに当たるケースを再現できませんでした。そのケースはユニットテスト(弾を直接配置)で確認済みです。
