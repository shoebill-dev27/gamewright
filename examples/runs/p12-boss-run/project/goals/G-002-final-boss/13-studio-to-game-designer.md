---
kind: handoff
goal: G-002
seq: 13
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 13: studio → game-designer — 旧集計の適用変更と新構成の試験対応を確定する

## Task

D-018の方向に基づき、D-006と関連基準のG-002新構成への適用変更を新しいDesigner Decisionで確定し、仕様§8を中心に補足する。保持・適用終了・置換する基準と試験、実測依存の判断を整理してStudioへ返す。

## Context

Ownerは「最後に手応えのあるボス戦がほしい」と依頼し、D-015で第1〜4部屋から第5部屋の単体ボスへ進む連続ランを承認した。D-017で詳細契約を定めたが、旧独立3〜5部屋・各3 hearts開始に依存する集計は、新ボスと回復付き連続ランの難度を同じようには測れない。

Game Directorは12とD-018で旧集計を過去記録として保存し、新構成の合否ゲートから外す方向を採択した。D-018はD-006自体を改訂していないため、担当権限による適用変更が必要である。完了後にTechnical DirectorのPlanへ進む。

## Findings

12の依頼を次の成果に具体化する。

1. D-006と正本step44について、新構成のゲートから外す部分を列挙する。walker合計3〜7 hearts・2/3 clear、関連するdodger／camper比較、FPS別の扱いを含める。過去G-001の判断・結果を保持し、適用変更はG-002の新構成に限定する。
2. 第1〜4部屋の構成、共有戦闘ルール、独立1〜2の比較、独立部屋の3 hearts開始条件、既存敵の回帰を保持する。独立3・4の各bot成績は30/60 FPS別に報告する。新しい数値ゲートを旧値から自動導出しない。
3. combat.mdの基準15について、独立3・4の既存規則を保持し、新5番でdashの有効性をどう検証するか定める。16cとBotsTestについて、独立1〜4の比較を保持し、新ボスのFPS比較に関する「同じclear結果・hearts差1以下」案の採否、前提、使用botの対応条件を確定する。この数値はDirectorによる採択済みではない。
4. 仕様§8の対応表に、旧構成依存の各基準・試験の保持・適用終了・置換先と理由を示す。旧集計のwalker／dodger／camper比較を含める。ボスの対処試験、独立Play、連続ランの到達・終端・時間計測との接続を明記し、テスト削除だけで解決しない。
5. 実測後に追加数値ゲートを判断する項目は、必要な計測、判断時点、Designerへの再判断経路を明示する。適用整理の完了と難度・体験の検証済みを区別する。

旧fixture維持は必須ではない。共有回帰への限定利用は可能だが、新構成の難度評価の代わりにはしない。

実行成功、指定sha一致、難度、所要時間について新しい証拠はない。

## Decisions already made

- D-006：旧独立3〜5部屋の集計基準。新Decisionによる適用変更までは存続する。
- D-015：Ownerが連続ラン、第5部屋の単体ボス、ラン先頭からのretryを承認。
- D-016：読み取り・位置取り・回避後の反撃を中心とする方向。
- D-017：二攻撃、境界回復、継承、終端、時刻、表示の詳細契約。未実装・未検証。
- D-018：旧集計を新構成の評価から分離する方向。詳細な適用変更と関連基準はDesignerが確定する。

## Constraints

既存Decision本文は編集せず、新Decisionに変更対象、適用範囲、旧Decisionとの関係を明記する。過去G-001の判断・結果を改変しない。

Owner requestとInterpretation、第1〜4部屋の構成、共有戦闘ルールを維持する。新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は追加しない。

15〜20分のVisionを維持する。時間合わせだけのHP増加や待機の水増しを行わず、独立部屋の時間合算を連続ラン実測と扱わない。

技術方式、実装順序、工数、実機入力経路の実現方式はTechnical Directorに残す。必要なDecision変更とPlanの完了前にBuildは開かない。

独立QA、限定Art Verify、独立Play、Reviewを維持する。Playtester向け資料はStudioが別途作成し、設計上の期待結果やReview用体験信号を渡さない。

## Open questions

- 適用終了する旧基準と保持する回帰を、関連比較・FPS別の扱いまで網羅できるか。
- ボスのdash検証と対応botのFPS比較案をどの条件で採用するか。
- 実測後に判断すべき数値基準は何で、誰がいつ再判断するか。

承認範囲を超える費用・リスク、Owner Decisionの変更、範囲内では解消できないVisionとの不整合が具体化した場合は、判断を確定せずStudioへ返し、Game Directorの判断につなぐ。

## Expected output

新しいDesigner Decisionと仕様補足を作成し、変更した文書、各基準・試験の対応、採否の理由、実測依存と再判断経路を記したHandoffを `to: studio` で返す。

Studioは適用変更に未解決の権限衝突がないことを確認してPlanを開く。Technical Directorへ渡す事項には、仕様§10の依存、指定sha `27fe16268ac8` と対象ビルドの同定、0.4／0.6表記差、実行基線、長時間実行・pause／resume・retry・時刻と入力・表示と境界試験の観測経路、工数とリスクを含める。追加数値ゲートの実測後判断が残る場合は、後続計画にその計測と再判断を組み込める形にする。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#current-state
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: goals/G-002-final-boss/10-game-designer-to-studio.md
- Project: repo/tests/test_game.py
- Project: repo/bots.py
- Project: repo/manual.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Previous handoff: goals/G-002-final-boss/12-game-director-to-studio.md
