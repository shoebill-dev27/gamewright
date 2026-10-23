---
kind: handoff
goal: G-002
seq: 24
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 24: gameplay-engineer → studio — 基線成功を記録し、実装対象ソースの供給を求める

## Task

Studioは現状repo/の実装ソースとテスト全文を次のBuildパケットへ含め、Gameplay Engineerへ再ルーティングする。D-021によるBuild開始承認を維持し、実装・変更後試験を継続する。

## Context

23は、既存テキストビルドで連続ランと第5部屋単体ボスを実装し、結果をstudioへ返す指示である。仕様と技術計画は提供されている。

本パケットにはrepo/manual.mdと基線のtests結果がある一方、変更対象のgame.py、play.py、bots.py、既存テスト本文がない。executor-instructionsにより、提供パケット以外のプロジェクト内容を仮定して実装しない。

## Findings

### 取得済みの実行基線

@run-resultsのRound 1に以下が記録されている。

- コマンド：`python3 -m unittest discover -s tests`
- Exit：0
- 件数：69 tests
- unittest所要時間：0.195秒
- 実行結果：OK

これは変更前の基線である。変更後の成功、ボス・連続ランの実装済み、30/60 FPS別の受け入れ基準合格を示さない。結果本文から各試験のFPS対応は確認できない。

### 実装前に照合したプレイヤー可視変更

追加する挙動の仕様上の根拠は以下のとおりである。

| 変更 | 正本 |
|---|---|
| 通常ランの1→5進行、1秒のクリア表示、入場時1 heart回復と状態初期化 | 最終ボス仕様§2 |
| B単体、HP12、固定照準の突進と短射、交互順序、非中断、回復 | §3 |
| 死亡優先、残弾消去、終端凍結、先頭retry | §4 |
| 両ゲーム時刻、pause/resume、試行別入力、unfinished | §5、計画16§3 |
| ボスHP・攻撃名・危険範囲・回復・進行・終端の表示 | §6 |
| 公開観測に基づく対応botと同一試行の測定 | §8〜9、計画16§8 |

現時点でDesigner判断を要する新たな仕様質問は特定していない。

### 具体的な不足と影響

次の現状ファイル全文が必要である。

- `repo/README.md`
- `repo/game.py`
- `repo/play.py`
- `repo/bots.py`
- `repo/tests/test_game.py`
- 上記が参照する追加ローカルモジュール、部屋データ、その他の既存テストがあれば、その全文

既存のクラス・更新順・関数契約・parser・公開観測・テストassertが不明なため、計画の「既存戦闘の外側に進行管理を置く」実装や共有コード経路の修正を具体化できない。ソースを推定して全置換すると、第1〜4部屋と共有回帰を維持した証拠を失う。

本Stepではrepo/を変更せず、新規テスト・manual改訂も作成していない。追加の@runは要求していない。実装ソースなしで同じ基線試験を再実行しても、今回の不足は解消しない。

これはD-020の供給条件の再要求ではない。指定sha、実機、gamepad、費用見積もり、外部担当の供給は求めない。必要なのは承認済み変更を適用する現状ソース本文である。

## Decisions already made

- D-015〜D-017：連続ラン、単体ボス、回復、終端、先頭retryの範囲と契約。
- D-019：旧集計の適用終了、保持回帰、対応bot比較、実測後Designer判断。
- D-021：現状repo/とStudio内のテキスト・スクリプト実行でBuild開始。指定sha照合、実機ホスト、実gamepad、外部配員、人日見積もりは不要。

## Constraints

第1〜4部屋と共有戦闘ルールを保持する。新戦闘入力、ボス用チェックポイント、HPや待機による時間合わせを追加しない。

実装は計画の依存順に逐次進める。30/60 FPSの検証、独立QA、限定Art Verify、独立Play、Designer実測後判断、Reviewを維持する。

未実行・未確認を成功としない。秘密情報や環境変数値は供給資料・実行記録へ含めない。

## Open questions

Studio：上記の現状ソース全文をBuildパケットへ追加できるか。既存テストと同じ実行対象の内容を供給し、基線結果との対応を維持すること。

技術方式の再設計や仕様変更を求める質問はない。

## Expected output

Studioは不足するソースを含めてGameplay EngineerへBuildを再ルーティングする。D-021の開始判断や既に成功した基線試験の取得をやり直さない。

継続BuildではGame終端処理→ボス・弾属性→Session→parser・表示・説明→対応bots・測定の順に実装し、保持／終了／置換したassertの対応を記録する。変更後のtests、両FPSのtrace・bots、通常ランの同一試行記録と独立検証手順をstudioへ返す。QA合否・Goal達成は実装者が代行しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#art-direction
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/
- Project: 上記の追加ローカル依存ファイル
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-cues-visual-spec.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step59.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: 23に列挙されたD-001〜D-007、D-011〜D-012、D-015〜D-019、D-021
- Previous handoff: goals/G-002-final-boss/23-studio-to-gameplay-engineer.md
- Execution evidence: @run-results Round 1
