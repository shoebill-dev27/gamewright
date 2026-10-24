---
kind: handoff
goal: G-002
seq: 12
from: game-director
to: studio
stage: Design
outcome: done
---
# 12: game-director → studio — 旧集計の適用変更をDesignerで確定してからPlanへ進む

## Task

Game DesignerのDesign補足を開き、D-006と関連基準の適用変更を新しいDesigner Decisionおよび仕様補足として確定させる。その完了後、Technical DirectorのPlanを開く。

## Context

D-015は連続ランと第5部屋の単体ボスを承認し、D-016は読み取り・位置取り・回避後の反撃を重視する方向を定めた。D-017の詳細仕様により、旧独立3〜5部屋の集計を新構成へ適用できないことが具体化した。

今回の判断は方向と権限境界の整理であり、詳細基準、技術方式、QA合否、Goal達成を決めるものではない。

## Findings

make-decisionに従い、方向上の選択を `decisions/D-018-legacy-balance-gate-transition-direction.md` に記録した。Designer推奨の「旧集計を過去記録として保存し、新構成の合否ゲートから外す」方向を採る。

旧第5部屋と各3 hearts開始に依存する集計を、新ボスや回復付き連続ランへ移しても同じ難度を測れない。D-006の再計測条件にも該当する。旧fixture維持は新構成の難度評価にならないため必須にはしない。必要な共有回帰への限定利用は可能とする。

D-018はD-006を改訂しない。Designerには次を依頼する。

1. **Decisionの適用変更を確定する。** D-006と、その正本であるstep44のどの部分を新構成のゲートから外すかを列挙する。walker合計3〜7 hearts・2/3 clear、関連するdodger／camper比較、FPS別の扱いを漏らさず整理する。過去G-001の判断・結果は保持し、変更はG-002の新構成への適用に限定する。
2. **維持する範囲を明記する。** 第1〜4部屋、共有戦闘ルール、独立1〜2の比較、独立部屋の3 hearts開始条件、既存敵の回帰を保持する。独立3・4の各bot成績は30/60 FPS別に報告する。新たな数値ゲートを旧値から自動導出せず、必要性と判断時点を明記する。
3. **関連する置換案を採否付きで確定する。** combat.md15は独立3・4の既存規則を保持し、新5番ではdashの有効性をどう検証するか定める。16cとBotsTestは独立1〜4の比較を保持し、新ボスのFPS比較について同じclear結果・hearts差1以下という提案の採否、前提、使用するbotの対応条件を確定する。本Stepではその数値を採択していない。
4. **仕様と試験の対応を完成させる。** 仕様§8を更新し、旧構成依存の各基準・試験について、保持・適用終了・置換先と理由を明示する。旧集計のwalker／dodger／camper比較も対応表に含める。ボスの対処試験、独立Play、連続ランの到達・終端・時間計測への接続を記し、テスト削除だけで解決しない。
5. **未実測事項を残す。** 追加の数値ゲートを実測後に判断する場合は、必要な計測とDesignerへの再判断経路を明示する。基準の適用整理が完了した状態と、難度・体験が検証済みの状態を区別する。

現時点でOwner判断を必要とする具体的な衝突はない。D-015が置換対象とした旧第5部屋依存の基準を、担当権限で整理できる。Ownerの承認範囲、Vision、Goalの意味を変更する提案は行わない。

play／botsは実行していない。実装前の基準適用判断であり、実行成功、指定sha一致、難度、所要時間について新しい証拠はない。

## Decisions already made

- D-006：旧独立3〜5部屋の集計基準。Designerの新Decisionによる適用変更までは存続する。
- D-015：連続ラン、第5部屋の単体ボス、ラン先頭からのretryをOwnerが承認。既存Decisionの変更は担当権限で解決する。
- D-016：読み取り・位置取り・回避後の反撃を重視し、Visionと承認範囲を保持する。
- D-017：二攻撃、境界回復、終端、時刻、表示の詳細契約。未実装・未検証。
- D-018：旧集計を新構成の評価から分離する方向を採択。詳細な適用変更と関連基準はDesignerが確定する。

## Constraints

既存Decision本文は編集せず、新しいDecisionに変更対象と適用範囲を記録する。D-018をD-006の改訂完了と扱わない。

第1〜4部屋の構成、共有戦闘ルール、Owner requestとInterpretationを維持する。新しい戦闘入力、ボスチェックポイント、既存部屋の全面改修は追加しない。

15〜20分のVisionは保持する。時間合わせだけのHP増加や待機の水増しは行わない。独立部屋の時間合算を連続ラン実測にしない。

技術方式、実装順序、工数、実機入力経路はTechnical Directorに残す。独立QA、限定Art Verify、独立Play、Reviewを維持する。Playtesterへの資料に設計上の期待結果やReview用体験信号を転記しない。

## Open questions

1. Designer：D-006の関連比較を含め、適用終了する範囲と保持する範囲を新Decisionで確定できるか。
2. Designer：dash使用数とボス対応botのFPS比較の置換案を、どの条件で採択するか。実測後の判断が必要な項目は何か。
3. Technical Director：Design補足後、指定sha `27fe16268ac8` と対象ビルド、0.4／0.6表記差、実行基線を同定できるか。
4. Technical Director：長時間実行、pause／resume、retry、時刻・入力、実機操作、表示と境界試験を実現・検証する費用とリスクは何か。

Ownerへの質問は現時点ではない。承認範囲を超える費用・リスク、Owner Decisionの変更、または範囲内では解消できないVisionとの不整合が具体化した場合に、Game Directorへ戻す。

## Expected output

StudioはDesign補足を確定ルートとして開く。Designerは新しいDecision、仕様§8を中心とする補足、基準と試験の対応、残る実測依存をStudioへ返す。

Studioは適用変更に未解決の権限衝突がないことを確認してPlanを開く。追加数値ゲートの実測後判断が残る場合は、その計測・再判断を後続経路に明示する。

Technical Directorは仕様§10の依存、実現方式、観測・検証経路、工数とリスクを計画する。必要なDecision変更とPlanの完了前にBuildを開かない。承認超過が判明した場合は実装前にGame Directorへ戻す。G-002は進行中とする。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#current-state
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: goals/G-002-final-boss/10-game-designer-to-studio.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Previous handoff: goals/G-002-final-boss/11-studio-to-game-director.md
