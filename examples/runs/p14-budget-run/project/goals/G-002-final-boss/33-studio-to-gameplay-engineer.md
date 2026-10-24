---
kind: handoff
goal: G-002
seq: 33
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 33: studio → gameplay-engineer — 保存版を検証し、統合Buildと実測を完成する

## Task

保存済みrepo/のsuite実行から再開し、32の基準別残作業、対応bot、文書統合、同一試行の通常ラン測定を完成する。承認済み仕様・計画の範囲で実装し、結果をstudioへ返す。

## Context

OwnerのGoalは「最後に手応えのあるボス戦がほしい」。第1〜4部屋から単体ボスへの連続ラン、勝利・死亡・先頭retryを対象とする。

32は公開Session driver、dispatch、予兆描画、7試験、public-driver.mdを保存成果として報告したが、今回保存版は未実行である。供給済み89／95／98 tests成功記録を今回保存版へ帰属させない。実装残作業も残っており、独立QAの開始条件は満たしていない。

D-021の開始承認は有効。実行round枯渇は前Stepの制約であり、新しい仕様質問やOwner承認待ちではない。

## Findings

32の基準対応表と残作業を引き継ぐ。特に以下を完成する。

1. 保存版suiteを実行し、失敗があれば承認済み仕様に従って修正する。追加7試験を含む成功件数は実結果だけを記録する。
2. R1〜R5・C1：正規撃破による通常ランの1→5到達、境界入力、継承、入場時反応記憶初期化、公開表示を確認する。
3. B1〜B10、T1〜T4、C2・C3：不足試験を補完する。実勝利・実死亡からのretry、凍結、旧試行未来入力と反応記憶の破棄、pause中入力、予兆・保護・境界、勝敗と同フレームlimitを含める。
4. V1：表示契機、両時計、予兆と実弾、弾ID・消去理由・イベントbuild字段を正本と照合する。旧構文経路との契約適用、短射の発射・寿命・回復時刻、長時間イベント蓄積も確認する。判断に仕様変更が必要なら独断で補わず、具体的な質問を返す。
5. D-019：公開観測に基づくボス対応dodgerを実装し、独立5番の開始3／2 heartsを同一limit・方針で両FPS比較する。独立3・4は全bot×両FPSを報告し、保持対象の共有回帰を確認する。
6. manual／READMEへ公開経路の操作・実行方法を統合する。
7. 正規撃破による同一試行の通常ランを測定する。部屋別時間、1秒遷移、ボス入場hearts、被弾、回復中反撃、終端、retry、pause、処理実時間を対応付ける。シミュレーション時間・driver時間・処理実時間を区別する。

32が参照する不足事項は保存ソース、仕様、Plan16・20と照合する。保存されていない提案を既存成果と扱わない。

## Decisions already made

- D-017：二攻撃ボス、境界回復、死亡優先、先頭retry、両時計・表示契約。
- D-019：旧集計の適用終了と代替評価。対応botのhearts別FPS比較と実測後Designer判断。
- D-021：現状repo/とStudio内テキスト実行でBuildを進める。実機供給・指定sha照合・費用承認を再取得しない。

## Constraints

- 第1〜4部屋の構成と共有戦闘規則を保持する。
- 新戦闘入力、ボスcheckpoint、時間合わせのHP・待機、購入・外部委託・追加金銭を追加しない。
- 旧13集計を復活させない。独立1〜2比較、3・4のdash、独立1〜4のFPS比較など保持基準は正本に従う。
- 未実行を成功とせず、fixtureや独立部屋の合算を通常到達・通常ラン時間の証拠にしない。
- 実機対応検証済みとは報告しない。
- 独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。明白な対処不能・到達不能が判明した場合は、測定証拠を添えてstudioへ返す。
- 追加数値ゲートや体験上の調整要否はDesignerの権限。Engineerが新設しない。

## Open questions

新しい仕様質問・開始承認待ちはない。今回保存版の実行結果、基準別不足の解消、比較測定と通常ラン測定が未確定。

## Expected output

次の連番のgameplay-engineer → studio Handoffを作成する。

変更ファイル、正本の基準別対応と未達、実行対象のbuild識別、実行コマンドと実結果、両FPSのbot比較、同一試行の通常ラン測定条件・値、独立QAが再現できる手順を記録する。自己評価はSender assessmentへ分離する。

全成果が揃えばBuild完了として返す。未完了の場合は保存成果と残作業、実行済み・未実行、具体的な阻害要因を区別する。仕様の曖昧さや計画の不成立が判明した場合は該当箇所と必要な判断を示して返し、独断で変更しない。独立QAへの投入はStudioの次Routeで判断する。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/public-driver.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_run_driver.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/32-gameplay-engineer-to-studio.md
