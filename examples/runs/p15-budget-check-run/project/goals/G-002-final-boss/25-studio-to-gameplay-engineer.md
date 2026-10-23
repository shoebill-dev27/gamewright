---
kind: handoff
goal: G-002
seq: 25
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 25: studio → gameplay-engineer — 現状ソース全文を用いてBuildを継続する

## Task

以下のLoadに明示した現状ソース全文を用い、承認された最終ボス・連続ラン仕様をrepo/へ実装する。D-021を優先し、16・20の適用可能な技術計画に従って変更・試験を行い、結果をstudioへ返す。

## Context

OwnerのGoalは「最後に手応えのあるボス戦がほしい」。23のBuildは、変更対象ソースがパケットになかったため24でquestionとして返された。仕様の曖昧さや計画不成立は報告されていない。

今回のRouteのInputsにはrepo/README.md、game.py、play.py、bots.py、tests/test_game.py全文が供給された。これらを次のBuildパケットへ本文として含めるため、Loadを個別ファイルで指定する。ディレクトリ名だけで全文供給済みと扱わない。

## Findings

24に報告された変更前の基線：

- `python3 -m unittest discover -s tests`
- Exit 0、69 tests、0.195秒、OK。
- 証拠の所在は前Stepの`@run-results Round 1`。本Handoffは24の報告を引き継ぐもので、Studioによる再実行ではない。
- repo/の変更、新規テスト、manual改訂は行われていない。
- この基線は変更後合格や30/60 FPS別の全基準合格を示さない。

今回供給されたソースのimportは標準ライブラリとローカルのgame・play・botsであり、部屋データはgame.py内にある。提供本文から、別のローカル実装モジュールを要する参照は見つからない。追加依存や別テストを実際に発見した場合は具体的なパスを示し、不存在や供給済みを推測しない。

repo/での実行経路：

- `python3 -m unittest discover -s tests`
- `python3 play.py --view player {script}`
- `python3 play.py --view trace {script}`
- `python3 bots.py {script}`

スクリプト構文はrepo/manual.mdを正本とし、未実装の計画構文を現行で使用可能と扱わない。今回提供されたソースを変更対象とし、既に報告された同じ基線の再取得だけを目的に作業を戻さない。対象内容の差異や既存失敗を発見した場合は分けて記録する。

## Decisions already made

- D-001：戦闘入力はattackとdash。
- D-002〜D-007、D-011〜D-012：既存接触・保護・予兆・文言・部屋構成の保持対象。新構成への適用はD-017・D-019に従う。
- D-015〜D-017：連続ラン、第5部屋単体ボス、回復、終端、先頭retryと詳細契約。
- D-018・D-019：旧第5部屋依存の集計を終了し、保持回帰、対応bot比較、実測後Designer判断を適用する。
- D-021：現状repo/とStudio内のテキスト・スクリプト実行でBuildを進める。指定sha照合、実機ホスト、実gamepad、外部配員、人日見積もりの取得は不要。追加金銭支出は認めない。

## Constraints

第1〜4部屋と共有戦闘ルールを保持する。新戦闘入力、ボス専用チェックポイント、既存部屋の全面改修、時間合わせだけのHP増加や待機を追加しない。

実装は逐次とし、Game終端処理→ボス・弾属性→Session→parser・表示・説明→対応bots・測定の依存順を守る。16・20中の実機ホスト・実機供給・外部検証枠・見積もり取得要求はD-021により今回適用しない。

30/60 FPS、独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。未実行・未確認を成功と扱わない。秘密情報・環境変数値・個人情報を成果や実行記録へ含めない。

## Open questions

- 承認仕様に従う連続進行、継承、ボス二攻撃、勝敗、pause、先頭retryの実装と試験結果。
- 保持／終了／置換する旧assertと新試験の対応、両FPSの共有回帰。
- 公開観測に基づく対応bot、独立部屋比較、通常ランの同一試行による到達・終端・時間記録。
- 実装中に具体的な仕様未確定や技術上の不成立が判明するか。

## Expected output

実装、必要な試験、manual／README更新、およびstudio宛ての結果Handoffを作成する。変更ファイル、基線と変更後結果、実行コマンド、入力script、30/60 FPS別の基準対応、旧assert移行表、未実施項目、独立検証用の再現手順を記録する。

対応botは開始hearts3／2を分け、clear／death／unfinishedと条件を報告する。通常ランは正規敵を実際に撃破した同一試行の到達・終端・時間を記録し、独立部屋の合算や加速実行の処理時間を人間のプレイ時間と呼ばない。明白な対処不能・到達不能はDesignerへ戻す根拠を示す。

実装者自身の評価・原因推定・確信度は`## Sender assessment`へ分離する。QA合否やGoal達成を代行しない。仕様不明ならDesigner、計画不成立ならTechnical Directorへの差し戻し理由を記し、studioへ返す。

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
- Project: repo/tests/test_game.py
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
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/24-gameplay-engineer-to-studio.md
