---
kind: handoff
goal: G-002
seq: 81
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 81: studio → technical-director — E1連続partialを受けた実行単位の再計画

## Task

68のE1残作業を、実際の供給上限内で完了を確認できる直列の実行単位へ分割・再計画する。実dodger接続と被弾差の診断を前進させる計画を作り、studioへ返す。今回コード実装・測定・QA判定は行わない。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。連続ランと最終ボスは実装報告済みだが、公開情報限定botと独立検証の準備が未完了である。

E1は72・74・76で連続partialとなり、当時の予算超過規則により範囲判断・Owner費用判断を先行した。D-025・D-026で継続を再開した後も80は同じE1をpartialとして返した。現在85/123 operationsであり、同じ作業の連続partialに対する分割・再計画をここで行う。Ownerへの新しい供給質問はない。

## Findings

- 80ではbots.pyの突進被弾ログをshot診断から分離し、test_bots_boss.pyに試験1件を追加した。runtime Build checkはsource fc07c7db6383、161 tests、exit 0。これは独立QAではない。
- 両FPSの制御fixtureで通常命中1 frameのログを確認した。通常到達、公開情報限定方針、無傷接触消費やE2全体の成立を示すものではない。
- 実dodgerは旧経路のまま。choose_bossは未接続prototypeであり、旧_dangersはactive chargeの内部phase_leftを読む。
- 直接呼出・play_room・_Proxy・play_runの記憶所有と初期化、全分岐・共有補助経路の監査、判断根拠と実発行入力の証拠が未完了。
- 接続案の被弾差は未解決。生成・再生差、制御列、方針と実接触の差を区別する必要がある。ログ誤分類の修正を根因確定とは扱わない。
- E1/input-replayの必要本文は切断により未確認。suite成功で代用しない。
- 13試験ファイルの配布台帳は76を基礎とし、80の追加ID・更新配布を引き継ぐ。配布予定と検証済みを区別する。
- E2全体、E3〜E5、独立Q1〜Q6、限定Art Verify、独立Play、Designer実測後判断、Reviewは未完了。

## Decisions already made

- D-025：必須検証と独立評価を維持し、重複工程・存在しない資料の探索・追加の磨き込みを省く。歴史的確認不能を保持した後続工程条件は決定済みで、再審議しない。
- D-026：budget 123。上限を使い切った場合は追加作業を開かず、範囲か費用をOwnerへ返す。
- D-024：現行検証、現行内対照、記録精度での比較、歴史的確認不能を分離する。
- 68：E1完了後にE2→E3→E4→E5→独立QAを直列で進める。今回その技術的な分割・順序を再検討できるが、仕様・必須成果は変更しない。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goal解釈を変更しない。既存hits0 assertを理由なく緩和せず、旧成績へ合わせる調整を計画しない。

各Stepは@run最大3回、各出力最大2万字、@need一度最大8ファイル。全文保存先、変更前ビルド、追加環境、外部配員、購入を前提にしない。出力切断・未表示・未実行を確認済みにしない。

独立QAと体験評価を実装者の自己試験で置換しない。60のfailは維持する。技術上成立しない具体的な条件があれば、その根拠と担当Roleへの手戻りを報告する。

## Open questions

1. これまでE1接続を完了できなかった技術的・作業分割上の原因は何か。
2. 実接続、互換診断、記憶・境界監査、判断出力を、依存を守りながらどの単位に分ければ完了を判別できるか。
3. 各単位に必要な個別本文、実行枠、表示範囲、失敗時の戻り先は何か。
4. 80の診断修正を再利用し、重複作業を避けつつE2以降へ進むための残条件は何か。

## Expected output

studio宛のHandoffに、変更対象、順序付き実行単位、各単位の入力・完了条件・試験・必要証拠・失敗時の戻り先を記す。次のEngineer Stepを具体的に開始できるLoad案を個別ファイル名で示す。

接続や監査を実施済みとはせず、計画と確認事実を区別する。未解決の被弾差と切断本文を明示し、同じ未検証案の反復を防ぐ判別条件を設ける。後続必須工程と残予算への影響も示す。範囲・費用判断が必要なら技術上の根拠を添えて返す。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/bots.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Evidence inventory: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Supporting report: goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
- Previous incoming task: goals/G-002-final-boss/79-studio-to-gameplay-engineer.md
- Previous handoff: goals/G-002-final-boss/80-gameplay-engineer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Decisions: decisions/D-025-g002-minimum-remaining-scope.md
- Decisions: decisions/D-026-owner-extends-g002-budget.md
