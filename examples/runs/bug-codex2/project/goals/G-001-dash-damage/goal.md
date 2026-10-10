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
- Diagnose / Plan: 共有無敵フラグの解除競合の診断と発生源別保護の計画は完了。追加 Plan の結果 `19-technical-director-to-studio.md` は、既存モデルの取得可否に応じた条件付き検証計画であり、入力取得や検証の完了ではない。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して継続する Owner の決定。D-003 は既存仕様を維持する技術方式の決定。
- Design: QA によれば期待挙動と受け入れ条件は明確。ただしクールダウン起点の原資料による回復は未確認。期待挙動が未定義または矛盾すると QA が判断した場合は game-designer に戻す。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。
- Build: `15-gameplay-engineer-to-studio.md` に模擬実装変更を定義済み。`17-gameplay-engineer-to-studio.md` の照合報告に基づき、`sim/build-0.4.md` を変更識別子 `0.3-G001-15` の模擬ビルドとして扱う。ファイル名を合わせるための再生成は不要。
- Verify: Build 後は必須。独立 QA が既存仕様・AC・模擬ビルドから文書評価可能な範囲と証拠の十分性を判断する。PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せ、AC-1〜AC-6 と必要な回帰を維持する。条件別試行資料は未取得であり、文書評価を試行実施と扱わない。
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
| 6 | Build | gameplay-engineer | implement-change | done | 14-studio-to-gameplay-engineer.md |
| 6b | Build 資料照合・補完 | gameplay-engineer | implement-change | done | 16-studio-to-gameplay-engineer.md |
| 6c | Plan 検証成立性の再検討 | technical-director | technical-plan | done | 18-studio-to-technical-director.md |
| 7 | Verify 文書評価・証拠充足性確認 | qa | verify-change | open | 20-studio-to-qa.md |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。行 2 の結果は `13-technical-director-to-studio.md`（done）。独立した Plan 行 5 は行 2 に統合したため skipped。

行 6 の結果は `15-gameplay-engineer-to-studio.md`（done）。変更記述を模擬実装とするプロジェクト規約に従う完了であり、simulator の資料生成や独立 Verify の合格を意味しない。

行 6b の結果は `17-gameplay-engineer-to-studio.md`（question）。done は照合と不足の報告が終了したことを示し、検証入力の完成を意味しない。

行 6c の結果は `19-technical-director-to-studio.md`（done）。条件付き計画の作成が終了したことを示し、モデル照会、資料生成、QA 判定は未実施である。

## Route changes

2026-10-10 — `02-qa-to-studio.md`（question）を受領し、1 を done とした。再現条件不足により追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（question）を受領し、1d を done とした。同じ不足入力について新しい該当資料がないまま question が二回以上返ったため、loop limits を適用した。`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を D-002 に記録し、09 を resolved、Goal を active とした。Observe 1e を追加した。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねた。

2026-10-10 — `11-qa-to-studio.md`（done）を受領し、1e を done とした。QA は不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。Diagnose と Plan を行 2 に統合し、行 5 は skipped とした。Build と Verify は維持した。

2026-10-10 — `13-technical-director-to-studio.md`（done）を受領し、行 2 を done、行 6 を open とした。D-003 に基づく方式と実装順序を technical-director の判断として引き継いだ。実装は逐次、完了後に独立 QA の Verify を行う。視覚変更は計画にないため art-director の追加は不要。

2026-10-11 — `15-gameplay-engineer-to-studio.md`（done）を受領し、行 6 を done とした。模擬実装の定義は完了したが、指定生成先 `sim/build-0.3-G001-15.md` と `sim/qa-G001-15.md` は存在一覧になく、検証入力が揃ったとは判断できなかった。一方、一覧には `sim/build-0.4.md` があったため、行 6b を追加して既存資料の照合・補完を依頼した。Verify は planned のまま維持した。

2026-10-11 — `17-gameplay-engineer-to-studio.md`（question）を受領し、行 6b を done とした。工程担当の照合報告に基づき、build-0.4 と変更識別子 `0.3-G001-15` の対応を採用する。ファイル名の違いは解消済みとして扱う。一方、条件別試行記録、試行生成用の既存モデル、クールダウン起点は不足している。実装への同じ補完要求を繰り返さず、Build の計画不成立に対する return rule を適用し、行 6c を追加して technical-director に検証成立性を戻した。これは QA の fail や同一 AC の二回目の失敗ではない。

2026-10-11 — `19-technical-director-to-studio.md`（done）を受領し、行 6c を done、行 7 を open とした。本 packet の project.md、存在一覧、Handoff 19 には runtime 管理側の窓口・照会手段がない。取得経路の状態は「照会手段未確保」であり、管理側への照会を実施した、またはモデルが存在しないとは記録しない。

取得済みモデルを前提とする工程担当への再依頼は行わず、19 の文書評価分岐に沿って、独立 QA に既存資料で評価できる範囲と証拠不足の判断を依頼する。取得不能が確定したわけではなく、QA 相談はモデル取得可能性の調査を代替しない。Studio 自身を open の受信者にしない。

QA には Studio 作成の `20-studio-to-qa.md` を渡す。前 Handoff 19 は Load に明記し、参照範囲を `Constraints` と `Open questions` に限定する。実装理由・原因説明・自己評価を含む工程担当 Handoff 全文は渡さない。仕様・AC 原文と模擬ビルドを評価対象とし、未生成資料は Load に入れない。

今回は仕様・AC・証拠要件の変更、Verify の合否判断、Owner escalation は行わない。QA が必須証拠の不足を返した場合、同じ不足の照会を無変更で反復しない。Role が解消できない必須外部入力または Goal の再解釈が必要と判明した段階で、該当する escalation trigger を適用する。

## Next action

QA が新しい独立した実行コンテキストで `20-studio-to-qa.md` を開始し、仕様・AC と模擬ビルドの対応、評価可能な範囲、条件別の証拠不足、仕様上の未解決事項を Studio に返す。

runtime の照会手段は未確保である。QA の判断を受けて、Studio が具体的な資料取得、必要な Design、または外部入力に関する Owner escalation を手配する。資料不足を修正完了や試行合格に読み替えない。

## Outcome

未完了。仕様不一致の確認、受け入れ条件、技術計画、模擬実装変更の定義、および更新ビルドの識別が完了した。D-002 に基づき継続し、D-003 の発生源別無敵管理が反映されたとの照合報告を受領した。条件付き検証計画の作成を終え、独立 QA に文書評価と証拠の十分性の判断を依頼する。条件別観察資料は未取得であり、独立検証の合格は未確定。現時点で Owner に新たな判断を求める事項はない。
