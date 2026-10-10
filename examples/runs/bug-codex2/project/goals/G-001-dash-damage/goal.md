---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-10
---
# G-001: ダッシュ中の被ダメージ不具合を修正する

## Owner request

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

## Interpretation

報告された被ダメージを再現し、仕様に反する挙動を修正して、ダッシュ時のダメージ判定が既存の仕様どおりに動くことを独立した検証で確認する。

戦闘の方向性変更、新しい入力の追加、無関係なバランス調整は対象外。

## Unknowns

- Observe: QA は既存仕様と模擬ビルドの記述から仕様不一致を確認し、不具合報告と AC-1〜AC-6 を作成した。Owner の詳細条件を独立した試行で再現したわけではない。追加 Observe は現時点では不要。
- Diagnose / Plan: technical-director が実装資料に基づき、共有無敵フラグを各タイマーが解除する競合を診断し、発生源別に保護を管理する修正計画を作成した。結果は `13-technical-director-to-studio.md`。実行による再現や修正は未実施。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して継続する Owner の決定。D-003 は既存仕様を維持する技術方式の決定であり、ゲームの方向変更ではない。
- Design: QA によれば期待挙動と受け入れ条件は明確。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。判断が必要になれば game-designer に戻す。
- Build: 計画と D-003 に従い模擬修正を具体化する。両ダメージ経路、再現用配置、既存クールダウン起点、試行資料を確認する。
- Verify: Build 後は必須。更新された模擬ビルドと観察資料を用い、AC-1〜AC-6 を PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せで独立検証する。
- Play: 体験や感触の改善依頼ではないため省略。
- Review: 体験 Goal やゲームの方向 Decision を伴わないため省略。
- Next: 検証後に Studio が Owner 向けの結果と残件をまとめる。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | 01-studio-to-qa.md |
| 1b | Observe | qa | reproduce-defect | done | 03-studio-to-qa.md |
| 1c | Observe | qa | reproduce-defect | done | 05-studio-to-qa.md |
| 1d | Observe | qa | reproduce-defect | done | 07-studio-to-qa.md |
| 1e | Observe | qa | reproduce-defect | done | 10-studio-to-qa.md |
| 2 | Diagnose / Plan | technical-director | technical-plan | done | 12-studio-to-technical-director.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | skipped | — |
| 4 | Design | game-designer | write-design-spec | skipped | — |
| 5 | Plan | technical-director | technical-plan | skipped | — |
| 6 | Build | gameplay-engineer | implement-change | open | 14-studio-to-gameplay-engineer.md |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（outcome: done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。行 2 の結果は `13-technical-director-to-studio.md`（outcome: done）であり、診断・計画の完了を表す。いずれも修正完了や Verify 合格ではない。独立した Plan 行 5 は行 2 に統合したため skipped。

## Route changes

2026-10-10 — `02-qa-to-studio.md`（question）を受領し、1 を done とした。再現条件不足により追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（question）を受領し、1d を done とした。基本資料は補完されたが、繰り返し求めている補足観察資料と実行環境側の回答は未提供で、追加再現確認は未開始。同じ不足入力について新しい該当資料がないまま question が二回以上返ったため、loop limits を適用した。過去の再ルーティング方針を修正し、`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を D-002 に記録し、09 を resolved、Goal を active とした。Observe 1e を追加し、`10-studio-to-qa.md` を open とした。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねた。

2026-10-10 — `11-qa-to-studio.md`（done）を受領し、1e を done とした。QA は不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。Diagnose と Plan を technical-director の一つの Step に統合し、行 2 を `12-studio-to-technical-director.md` で open とした。行 5 は統合により skipped。Build と Verify は維持した。当時の packet にない実装資料・設計・Decision・契約・Skill の本文を読んだとは扱わず、次の Step の Load に指定した。

2026-10-10 — `13-technical-director-to-studio.md`（done）を受領し、行 2 を done とした。診断・計画が予定した Build の入力を満たすという担当の報告を受け、行 6 を `14-studio-to-gameplay-engineer.md` で open とした。D-003 に基づく方式と実装順序は technical-director の判断として引き継ぐ。実装は逐次、完了後に独立 QA の Verify を行う。視覚変更は計画にないため art-director の追加は不要。

新しい Owner escalation の根拠はない。本 Route packet には gameplay-engineer の Works from はあるが、契約全文・Skill・設計・実装資料・Decision・QA 報告の本文は含まれない。これらの内容を確認済みとは扱わず、次の Step packet に Load 資料として要求する。欠落や矛盾があれば具体的に報告し、推測で実装しない。

## Next action

新しい executor で gameplay-engineer が `14-studio-to-gameplay-engineer.md` とその Load 資料から Build を開始する。模擬修正の内容、変更対象、試し方、simulator が更新する資料と観察要件を Handoff に記し、結果を Studio に返す。

Studio はその結果と模擬資料の更新を確認してから、実装者の自己評価・理由を除いた入力で独立 QA に Verify を依頼する。本 Route では Build や Verify を実行しない。

## Outcome

未完了。QA による仕様不一致の確認と受け入れ条件の作成、technical-director による資料上の原因診断と修正計画が完了した。D-002 に基づき継続し、D-003 の発生源別無敵管理を Build に渡した。独立した詳細再現、修正、修正後の検証はまだ完了していない。現時点で Owner に新たな判断を求める事項はない。
