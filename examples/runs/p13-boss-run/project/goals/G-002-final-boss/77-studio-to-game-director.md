---
kind: handoff
goal: G-002
seq: 77
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 77: studio → game-director — 予算超過後の残作業をOwner requestへ絞る

## Task

残作業を「最後に手応えのあるボス戦がほしい」に必要なものへ絞る。継続必須・省略可能な工程とその理由、終了条件を決定し、Owner Decision・Vision・Goal解釈の変更が必要ならOwner向けのエスカレーションを作成する。

## Context

Goalは80/40 operationsで予算超過。76で同じE1が連続partial 3回（72・74・76）になった。通常はTechnical Directorへ分割・再計画を戻すが、予算規則はそのループより範囲判断を優先する。Studioは内容上の省略を決めず、このStepを開く。予算はOwnerのResume以外では変更できない。

## Findings

- 製品の連続ランとボスは実装報告済みだが、独立QAの直近判定60はfailのまま。Goal達成のReviewはない。
- 76は再生互換診断と証拠helperの本文出力を保存した。runtimeはsource e99408d647c7、160 tests OKを報告した。必要な診断行の本文は未確認で、件数成功は受け入れ判定ではない。
- 実dodgerは旧判断経路を使い、非公開active残時間を参照する。公開境界prototype成功を実経路の適合には使えない。
- 公開境界接続、接続案の被弾差の原因確定、実経路の記憶・全分岐監査、判断列整備が残る。76は接続・互換診断・監査・証拠の4単位を提案しているが、方式は未決定。
- 従来計画68はE1の後に接触診断、ボス4条件再測定、保持回帰、通常ラン入力再生成、独立Q1〜Q6を予定する。さらに後続工程条件判断、限定Art Verify、独立Play、Designer実測後判断、Reviewが残る。
- D-024の歴史的確認不能は現行suiteで解消しない。対応前botの通常ラン時間約87／104秒は診断資料であり、対応後の基線やプレイヤー所要時間ではない。
- 新しい供給質問はない。追加環境、全文保存先、変更前ビルドは存在しない。

範囲判断の選択肢は、承認済み契約を維持して任意の重複作業・出力整備を絞ること、または必要な縮小がOwnerの承認事項に及ぶなら具体的な費用・範囲の選択をOwnerへ求めること。どの作業が削減可能かは本Stepが判断する。確認不足を合格に変える選択肢はない。

## Decisions already made

- D-019：公開情報限定bot、保持回帰、開始3/2 hearts別FPS比較、Review前のDesigner実測後判断。
- D-021：Studio内テキスト検証。独立QA・限定Art Verify・独立Playを別Stepで実施し、追加金銭を使わない。
- D-023：個別Load、@need一度最大8ファイル、@run最大3回、出力最大2万字。仕様・難度・Goal判断は変更していない。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離する。

## Constraints

Owner requestとInterpretationを変更しない。Owner-made Decision、Vision、予算の変更はOwnerへエスカレーションする。技術方式や詳細仕様、QAの合否を代行しない。

未確認・切断・未実行をpass、免除、適用終了へ変更しない。残りのplanned工程は本Stepの判断まで開かない。存在しない供給を再要求しない。

## Open questions

1. 承認済み契約の範囲で、Owner requestに必要な作業へ何を絞れるか。
2. 何を残し、何をskippedにできるか。その根拠と終了条件は何か。
3. 必須作業を維持すると追加の費用判断が必要か。必要ならOwnerが選べる具体的な選択肢は何か。
4. 歴史的確認不能を保持した後続評価の条件判断を、既存のplanned工程とどう整理するか。

## Expected output

範囲内で決められる場合はDecisionとstudio宛Handoffを作成する。残す工程・省略する工程・依存関係・終了条件を列挙し、未完了の技術課題を保持する。単に従来の全工程を再掲せず、削減できる作業と削減できない理由を明示する。

Owner権限が必要なら、日本語のEscalationを作成し、studioへ返す。供給事実を再質問せず、継続費用または承認変更について一つの決定を求める。Goal達成のReview verdictは今回の成果物としない。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
