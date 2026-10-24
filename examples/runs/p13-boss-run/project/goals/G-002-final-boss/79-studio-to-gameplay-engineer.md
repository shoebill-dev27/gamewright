---
kind: handoff
goal: G-002
seq: 79
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 79: studio → gameplay-engineer — 承認された上限内でE1残作業を再開

## Task

68の実行計画と76の引継ぎから、E1の実dodger公開境界接続、被弾差の診断、監査・判断証拠の未完了作業を再開する。今回の単位を既存計画内で明示し、完了した範囲と残作業をstudioへ返す。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。連続ランと最終ボスは実装報告済みだが、独立検証に必要な試験道具と証拠が未完了である。

E1は72・74・76で連続partialとなった。予算超過時のGame Director判断を77で開き、78で費用をOwnerへエスカレーションした。Ownerは案Aを選び、D-025で絞った範囲での継続とbudget: 123を承認した。本Stepはその範囲内の既存Buildを再開するものであり、新しい方向・技術計画をStudioが決めるものではない。

## Findings

- 76では再生互換診断とhelper本文出力を保存したと報告されている。実dodger接続、被弾差の原因確定、記憶・全分岐・判断出力は未完了。
- source e99408d647c7の160 tests OKは過去のruntime確認。現在のpacketが示すbuildはrepo/、sha 61492279ed13であり、過去の試験結果を現行確認として流用しない。
- 必要な診断本文は未確認。76の13ファイルQA配布台帳と追加ID、70の残作業を引き継ぐ。
- E2以降は未着手。E1未完了を成功扱いして先へ進めない。
- 旧botの約87／104秒は対応後の基線やプレイヤー時間として使用しない。

## Decisions already made

- D-026：Ownerが案Aを選択。累計83 operationsに40を加えbudget: 123。使い切ったら範囲か費用をOwnerへ再確認する。
- D-025：重複する後続条件判断、存在しない資料の再探索、旧構成の任意検証、重複整形と追加の磨き込みを省く。必須検証と独立評価は維持する。
- D-024：歴史的一致の確認不能を、現行仕様照合・現行内対照や記録精度での比較と区別する。確認不能を合格・免除にしない。
- D-021・D-023：テキストビルドとStudio内検証、実際の供給上限で進める。

## Constraints

- 承認済み仕様・難度・秒数ゲートを変更しない。曖昧な仕様や実行不能な計画は担当Roleへ手戻りを報告する。
- 各Stepの@runは最大3回、各出力は最大2万字。全文保存先は存在しない。必要な追加本文の@needは一度、最大8ファイル。
- 本文未確認、出力欠落、未実行を成功にしない。既存証拠の識別子と対象ソースを明記する。
- 変更前ビルド、追加環境、外部配員、購入、存在しない保存機構を要求しない。
- budget: 123は完成保証でも無制限継続でもない。上限到達時は追加作業を自動継続しない。
- QA判定、体験判定、Goal達成判定を行わない。

## Open questions

- 既存計画内で、E1の公開境界接続と被弾差の説明を成立させられるか。
- 接続・記憶・全分岐監査と判断証拠のうち、今回確認できた範囲と残る範囲は何か。

## Expected output

studio宛のHandoffを作成する。今回対象とした作業、変更ファイル、対象ソース、実行した確認と観測結果、証拠の識別子、QA配布台帳の更新、残作業を記す。

E1完了ならその根拠を示し、68のE2以降へ引き継ぐ。未完了ならpartialとして具体的な残作業を示す。既存計画が実行不能ならquestionとして技術上の理由を報告し、同じ未検証案を成功扱いして繰り返さない。独立QAに渡す事実と実装者の評価は分け、後者はSender assessmentへ置く。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/
- Decisions: decisions/D-025-g002-minimum-remaining-scope.md
- Decisions: decisions/D-026-owner-extends-g002-budget.md
- Plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Evidence inventory: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Previous implementation handoff: goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
- Previous handoff: goals/G-002-final-boss/78-game-director-to-owner.md
