---
kind: handoff
goal: G-002
seq: 21
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 21: studio → game-director — 供給・費用承認のOwner判断を具体化する

## Task

20の限定調査とbriefを基に、現行仕様を継続するための供給・費用承認について、一つのOwner Escalationを日本語で準備する。必要物、回答すべき権限者、未確定費用、選択後の経路を明記し、未確認を承認・供給不能へ読み替えない。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。D-015で連続ラン・単体ボス・先頭retryを承認し、D-016〜D-019で方向・仕様・基準適用を確定した。D-020による限定Plan補完は20で終了したが、Build開始の五条件は揃っていない。

回帰正本の読込みは解決した。一方、供給責任者、利用権、独立検証枠、予算承認根拠はパケットから生成できず、実行経路の確認も取得不能として返された。Studioは同じ不足だけの三度目のPlanを開かず、権限を持つ相手への具体的な判断準備へ進める。

## Findings

- 20の§1〜2：実行ツールの取得経路が利用できず、shell・Pythonは未着手。指定sha `27fe16268ac8`との一致、基線、版表記差の原因は未確認。このexecutorの制約はプロジェクト資源の不存在を示さない。
- 20の§3：回帰正本と実テストの保持・終了・置換対応を補完。D-020条件2はPlan上充足したが、実行合格ではない。
- 20の§4〜7：最小desktopホスト方式を提示したが、OS・表示環境、依存権限、keyboard／gamepad、独立QA・Art・Play枠の供給は未確認。pygame／SDL系は候補であり確定依存ではない。
- 暫定計画18〜33.5人日はBuild、独立検証、Designer判断、修正・再検証枠、Reviewを含む。金銭費用、日程、既消化工数との精算、環境対応増分は未確定。承認済み総額ではない。
- 20の§8は既存資源指定、不足分の調達を伴う継続、供給・承認まで停止の案を提示している。Studioはゲーム内容の選択や推奨を決定していない。

## Decisions already made

- D-015：連続ラン、第5部屋単体ボス、先頭retryのOwner承認。無制限の費用承認ではない。
- D-016／D-017：体験方向と詳細契約。headlessだけへの縮小やV2任意化は未承認。
- D-019：回帰適用、対応bot比較、Designer実測後判断を維持。
- D-020：最小実機ホストは既存要件の実現作業。五条件解決までBuild保留。費用承認根拠の取得不能などを再検討条件とする。

## Constraints

Owner requestとInterpretationを維持する。Goalの再解釈、範囲縮小、費用・権限・調達の承認はOwnerへ戻す。技術方式はTechnical Director、詳細仕様はDesignerの権限に残す。

実装、依存導入、購入、外部費用の確約、外部への連絡は行わない。人物名、予算上限、単価、供給可能性を創作しない。回答者が特定できない場合は、Ownerに供給責任者・予算権限者の指定を求める形にする。

予算不明を超過とも承認内とも扱わない。暫定人日幅を金銭総額・納期の確約にしない。秘密情報や個人情報を求めず、必要な権限・資源の非秘密の条件のみ扱う。

Build保留、逐次作業、独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

1. 読取・実行可能なcheckout、shell／Python、対象desktop・入力機器・依存利用権限、独立検証枠について、誰が供給と条件を回答するか。
2. 既存承認との照合資料を誰が提供できるか。取得不能なら、Ownerに今求める供給・承認条件は何か。
3. 既存資源を指定して継続、不足分の条件付き調査・調達準備、停止のうち、現時点で提示できる2〜3案と推奨は何か。未見積もりの購入を包括承認する案にはしない。

## Expected output

`studio/templates/escalation.md`に従う日本語のEscalationをOwner宛てに作成する。判断対象を「必要な供給・費用条件を整えて現行仕様を継続するか」にまとめ、Roleで生成できない必要物、権限者、既知の暫定幅、未確定部分、2〜3案、Game Directorの推奨と再検討条件、各案の後続ルートを示す。

供給情報の提出や責任者指定への同意と、未確定の購入・実装費用の承認を区別する。どの継続案でもD-020の五条件を満たす前にBuildを許可しない。範囲変更案を含める場合はOwnerのResume後にDesign／Planへ戻す。

Studioは提出されたEscalationを次のRouteでOwnerへ開き、依存Stepを停止してGoalをblocked-on-ownerにする。現Stepは判断準備であり、Owner承認を取得済みにしない。同じ資料のままPlanへ返さない。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: studio/orchestration.md
- Project: studio/templates/escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: goals/G-002-final-boss/18-game-director-to-studio.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
- Previous handoff: goals/G-002-final-boss/20-technical-director-to-studio.md
