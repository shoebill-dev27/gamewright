---
kind: handoff
goal: G-002
seq: 64
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 64: studio → game-designer — 変更前一致基準の証拠と扱いを確定する

## Task

変更前ビルドが存在しない条件で、変更前との一致を求める基準を個別に整理する。Ownerの指定に従い、記録数値との比較にするか、確認不能として扱うかを決め、後続の技術再計画と独立QAが使える基準を示す。

## Context

G-002は、既存第1〜4部屋から最終単体ボスへ進む連続ランを、repo/のテキスト方式で成立させるGoalである。Build後のQAでは検証資料・実行・ログ不足が二度報告され、Technical Directorが62で試験道具と証拠構成の計画を提出した。

Ownerは63に案Aと回答し、D-023で供給条件を確定した。変更前ビルドは保存されておらず、その供給を待つ計画は採れない。Ownerは変更前一致基準の扱いをDesignerに委ねた。今回はその判断を先行させる。実測後の難度・追加数値ゲート判断は別の予定Stepとして残る。

## Findings

- 現行buildはrepo/。操作packetの識別値はd86d55d41027。D-021により旧指定sha照合は要件ではない。
- 56のBuild報告には通常ラン勝利時間30 FPS 86.967 s／60 FPS 103.533 s、保存ソース04fa2b1c168aの全suite152件OKがある。これらは独立QAの合格でも変更前同一性の証明でもない。
- 60のQA結果、62の計画、正本仕様と関連Decisionから、L1/O3を含む該当基準を特定すること。数値の意味、測定条件、精度を本文で確認してから比較可能性を判断する。
- ボスbotの非公開active残時間の参照について対応計画がある。対応前の比較値を新たな合格根拠にしない。製品戦闘の不具合や難度不合格と同一視しない。

## Decisions already made

- D-021：テキストビルドとStudio内の別Stepによる独立検証で進める。
- D-019：旧集計の適用関係と代替評価を定める。具体的内容は本文を参照する。
- D-022：V1補足を定める。具体的内容は本文を参照する。
- D-023：案Aを選択。変更前一致基準を記録数値との比較にするか確認不能として扱うかはDesignerが決める。

## Constraints

- 製品仕様、戦闘パラメータ、難度、秒数ゲートを供給不足だけを理由に変更しない。
- 記録数値との一致から、保存されていない変更前実装との厳密な同一性を主張しない。
- 確認不能は合格・免除・Goal達成と区別する。Goalの再解釈や範囲縮小が必要なら、権限を越えて決定せず手戻り理由を示す。
- Loadは個別ファイル本文が届く。ディレクトリ指定はファイル名だけ。追加本文は@need一度、最大8ファイルまで。
- @runはStepあたり最大3回。出力は先頭と末尾を含む最大2万字で、全文保存先も別実行枠もない。必要なら検証対象を絞った出力を使う。
- 実機、gamepad、外部配員、追加金銭、存在しない変更前ビルドを要求しない。
- 実装やQA判定は今回行わない。

## Open questions

- 変更前一致を要求する基準はどれか。それぞれどの記録を使えるか。
- 記録比較が成立するものの測定条件、精度、比較方法、証明できる範囲は何か。
- 確認不能の項目を、後続QAと最終Reviewへどう明示して渡すか。

## Expected output

重要な判断を新規Decisionに記録し、必要なら正本仕様の該当箇所を更新する。各基準について、従来要求、採用する扱い、根拠資料、比較条件と精度、未確認として残る点を表で示す。

結果Handoffはto: studioとする。Technical Directorが62をD-023へ適合させるために必要な仕様上の入力と、追加で必要な個別ファイル名を明示する。QAへ直接免除を依頼しない。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/60-qa-to-studio.md
- Project: goals/G-002-final-boss/62-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Previous handoff: goals/G-002-final-boss/63-studio-to-owner.md
