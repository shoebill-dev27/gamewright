---
kind: handoff
goal: G-001
seq: 10
from: studio
to: qa
stage: Observe
outcome: routed
---
# 10: studio → qa — Owner の補足観察から不具合報告を更新する

## Task

Owner の新しい観察を既存の戦闘仕様と模擬ビルドに照合し、再現確認が可能な範囲を評価して不具合報告を更新する。確認できた事実、Owner の報告、未確認事項を区別し、修正に渡せる受け入れ条件と残る必須入力を Studio に返す。

## Context

G-001 の元の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」である。

これまでの Observe は補足観察資料が不足したまま `question` を繰り返したため、Studio は Owner にエスカレーションした。Owner は資料を補完して修正を継続する Option A を選び、下記の観察を提供した。今回の再開はこの新しい入力に基づく。

本プロジェクトは dry-run で、実機用リポジトリはない。「ビルドを実行する」とは `sim/build-0.3.md` を読むことである。

## Findings

Owner の回答原文：

> A。私のプレイでの観察です(計測ではなく体感)。部屋1〜2でGrubに噛まれたあと、硬直が解けてから少し間をおいて(被弾から体感0.5〜0.8秒くらい)ダッシュすると、ダッシュの後半で別のGrubに触れてハートが1減る。被弾直後すぐにダッシュした場合と、被弾していないときのダッシュでは起きない。60 FPSのPC・ゲームパッドで10回中6回ほど。Spitterの弾でも1回あった。30 FPSでは試していない。

この入力から得られるのは Owner が報告した発生条件と比較条件である。0.5〜0.8 秒、ダッシュ後半、10 回中 6 回ほどは計測結果として扱わない。「起きない」という比較条件も全条件での非発生保証ではない。

正確なイベント時刻、敵の総数、位置関係、ダッシュ方向、比較条件の試行数、Spitter の詳細条件、30 FPS とキーボードの結果は提供されていない。これらすべてを一律に再開条件とせず、仕様と模擬資料を読んで必要性を判断する。

Resume packet には `design/combat.md` と `sim/build-0.3.md` の本文が含まれていないため、Studio は今回それらの内容を再確認していない。QA の次の packet には Load に指定した本文が必要である。技術原因や独立した再現成功について Studio の判断はない。

## Decisions already made

- `decisions/D-002-resume-with-owner-observations.md` — Owner は Option A を選択し、部分的な観察を使って元の修正 Goal を継続する。仕様変更や修正完了の承認ではない。
- Project の既存制約：攻撃、ダッシュ、ポーズ以外の入力を Owner の承認なく追加しない。

## Constraints

- 既存仕様への不具合修正が対象。戦闘の方向性変更、入力追加、無関係なバランス調整は対象外。
- 対応条件は PC、キーボード・ゲームパッド、30 / 60 FPS。Owner の未試行条件を確認済みとしない。
- Owner の観察と模擬資料に存在しない測定値・試行結果を作らない。
- QA は仕様に対する再現性と受け入れ条件を判断する。実装原因の断定や修正方式の決定は行わない。
- 入力不能中の予約入力や完全同時の境界処理を、この Step で新しく仕様化しない。必要なら仕様上の質問として返す。
- 独立した新しい executor で実施する。実装者の説明・自己評価は入力に含めない。

## Open questions

- 既存仕様と模擬ビルドから、報告された被ダメージをどこまで独立して確認できるか。
- 被弾後に間をおいたダッシュ、直後のダッシュ、未被弾時のダッシュを比較するための手順と期待結果を、既存仕様から記述できるか。
- Grub 接触と Spitter の弾について、確認済み範囲と未確認範囲は何か。
- 修正に渡せる不具合報告と受け入れ条件を作れるか。作れない場合、不可欠な不足情報は何で、既存資料から得られない理由は何か。

## Expected output

次の Handoff を `to: studio` として作成し、Findings に次をまとめる。

- 資料と根拠を示した不具合報告：条件、手順、仕様上の期待結果、報告または確認された実際の結果。
- Owner の報告、模擬資料で確認できた事実、未実施・不明の範囲の明確な区別。
- 既存仕様に基づくプレイヤーから観察可能な受け入れ条件。30 / 60 FPS と両入力方式を含む後続検証の対象。
- Build に渡せるか、追加の調査や入力が必要かを判断できる具体的な残件。

評価を完了できれば `outcome: done`、必須資料や判断が不足して進めない場合は `outcome: question` とする。これは修正後の Verify ではなく、修正合格を宣言しない。資料不足の場合も、今回の観察で何が解消し、何がなお不可欠かを明記する。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Previous handoff: goals/G-001-dash-damage/09-studio-to-owner.md（Owner 回答を含む解決済み Escalation）
