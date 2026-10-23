---
kind: handoff
goal: G-002
seq: 29
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 29: studio → gameplay-engineer — 保存版を実行確認し統合Buildを完成する

## Task

28の部分成果を引き継ぎ、承認済み仕様と計画に従って統合Buildを完成する。まず現在の保存版を実行確認し、残る実装、試験、説明更新、対応botと通常ラン測定を行い、結果をstudioへ返す。

## Context

OwnerのGoalは「最後に手応えのあるボス戦がほしい」。既存第1〜4部屋を連続して進み、第5部屋の単体ボス、最終勝利・死亡・先頭からの再挑戦を成立させる。

26では終端基盤、28ではボス戦闘の部分実装が報告された。統合Buildは未完了であり、独立QAへはまだ渡さない。D-021の開始承認は有効で、新たな供給・実機・費用承認は不要。

## Findings

28が報告した保存内容は、HP12の第5部屋ボス、固定照準の突進／短射、弾の発射元と寿命、攻撃回復残値の正規化、種別分岐、旧5番assertの移行、ボス9試験である。現状ソースと試験で反映状況を確認すること。

提示されたRound 1は81 tests、1 failure／5 errorsだったが、今回保存版の結果ではない。今回保存版のtests・trace・botsは未実行であり、成功や攻略可能性の証拠として扱わない。

残作業は28の基準別一覧と再現手順を使用する。

1. `repo/`で `python3 -m unittest discover -s tests` を実行し、保存版の失敗・回帰を確認して対応する。
2. B1〜B10の不足試験と、弾ID・接触消費・消滅理由など必要な観測を補完する。
3. RunSessionとR／T／Cの契約を実装し、連続到達、境界、両時刻、pause、retry、limit、終端を統合する。
4. Plan16のmode、attempt、control、limit、driver-limit構文、player／trace表示、manual／READMEを完成する。内部イベントやtraceだけで公開表示の基準を満たしたとしない。
5. 公開観測に基づくボス対応dodgerを追加し、独立1〜4の既存方針を保持する。
6. 同一build・初期状態・方針・limitで、独立5番を開始hearts3／2別に30/60 FPS比較する。独立3・4は各bot・各FPS別に報告する。
7. 通常ランを正規敵撃破で実行し、同一試行の到達・終端、部屋別時間、遷移、ボス入場hearts、被弾、反撃、retry、pauseと処理実時間を記録する。独立部屋の合算やfixtureで通常ランの成立を代用しない。

仕様と計画が正本であり、この一覧は基準の省略や変更を許可しない。

## Decisions already made

- D-015〜D-017：連続ラン、第5部屋単体ボス、回復、死亡優先、先頭retry。
- D-019：旧集計の適用終了、共有回帰保持、対応bot比較、実測後Designer判断。
- D-021：現状repo/のテキスト表示・スクリプト実行とStudio内の独立検証を使用。実機供給、指定sha照合、人日見積もりを開始条件にしない。

## Constraints

第1〜4部屋の構成と既存共有戦闘ルールを保持する。新しい戦闘入力、ボス専用チェックポイント、時間合わせのHP・待機追加は行わない。購入・外部委託・追加金銭を使わない。

30/60 FPSを扱う。D-019による旧集計終了を、共有回帰やボスFPS比較の免除と解釈しない。

独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。自己試験で独立検証を代替しない。明白な対処不能・到達不能を確認した場合は証拠を添えて返し、Designer判断の前倒しを可能にする。

## Open questions

新規仕様質問・開始承認待ちはない。実装中に仕様の曖昧さ、計画の不成立、承認範囲を超える変更が具体化した場合は、該当箇所と証拠を示して手戻しする。

## Expected output

次の連番のGameplay Engineer→studio Handoffに、完成範囲、基準別の対応、変更ファイル、実行コマンドと実際の結果、未達事項、測定条件と値、独立QAが再現できる手順を記録する。

完了・未完了と未実行を明確に区別する。自己評価・原因説明は `## Sender assessment` に分離する。完成したBuildでも合格判定は独立QAに委ねる。未完了なら残作業と具体的な阻害要因を明記する。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
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
- Previous handoff: goals/G-002-final-boss/28-gameplay-engineer-to-studio.md
