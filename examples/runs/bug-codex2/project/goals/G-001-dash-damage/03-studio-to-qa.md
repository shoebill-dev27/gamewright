---
kind: handoff
goal: G-001
seq: 3
from: studio
to: qa
stage: Observe
outcome: routed
---
# 03: studio → qa — 補足観察資料による再現条件の確認

## Task

補足観察資料が提供されたら、被弾後のダッシュ中に再被弾する条件を確認し、再現手順と受け入れ条件を備えた不具合報告を完成させる。資料が不足したままの場合は条件を推測せず、確認できない項目を明示して Studio に返す。

## Context

Owner の依頼：

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

初回 QA は模擬資料と既存仕様の不一致を報告したが、具体的な再現条件が不足しているため `outcome: question` で Studio に返した。Studio は追加 Observe を次のステップとし、Build はまだ開始しない。

## Findings

前回の QA 報告は `02-qa-to-studio.md` に記録されている。

- QA によれば、既存仕様はダッシュの全期間 0.25 秒を無敵と定める。
- 模擬ビルドには、被弾後にダッシュすると時折その途中でダメージを受けるとの記述がある。
- 敵・攻撃種別、配置、入力と命中の時系列、試行数、入力方式・FPS ごとの結果は不足している。
- 前回の報告には既存仕様に基づく受け入れ条件がある。検証済みという意味ではない。

今回の Route では新しい観察結果を取得していない。補足資料は未提供であり、これが追加観察の blocker である。

実行前に、模擬ビルドの観察資料として以下を補足する必要がある：

- 部屋、敵の種類・数、命中源、位置関係、ダッシュ方向。
- 初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の時系列。
- 条件ごとの試行数と発生数、および比較条件。
- キーボード／ゲームパッド、30／60 FPS の設定と観察範囲。

資料の所在と入手方法は現 packet では確定できない。Studio が観察結果を創作したり、補足済みと扱ったりしてはならない。

## Decisions already made

この Goal での新しい Decision はなし。

既存仕様への修正として進める。QA の報告では期待挙動は明確であり、Design は省略する。入力追加や戦闘の方向変更は対象外。

## Constraints

- Dry-run project であり、実在の repository はない。資料の読解と実機での実行確認を区別する。
- 実装や技術的原因を推測して再現条件を補わない。
- 未観察の条件を確認済みと扱わない。
- 入力不能中のダッシュ予約や完全同時の境界処理を新たに規定しない。
- QA は独立した executor で実施し、実装者の自己評価や理由説明を受け取らない。
- 下記 Load の完全な本文と補足観察資料が用意されるまで、同じ資料だけの再試行を行わない。

## Open questions

- どの配置と操作で再現し、何回中何回発生するか。
- 初回被弾とダッシュ、再被弾の時間関係はどうなっているか。
- 被弾からダッシュまでの間隔を変えると、発生条件はどう変わるか。
- 攻撃種別、入力方式、FPS による差はあるか。
- 補足観察資料を実行環境から提供できるか。

## Expected output

補足資料がそろえば、QA は再現手順、観察結果、再現性、重大度、受け入れ条件、未確認範囲を含む不具合報告を `to: studio` の Handoff として返す。

資料が提供できなければ、不足資料と、その不足によって確定できない事項を `outcome: question` で Studio に返す。修正済み、再現確定、検証合格とは扱わない。

## Load

以下は次の Step に必要な入力。今回の Route packet にない本文と補足資料は、実行環境側で用意する必要がある。

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Project: 補足観察資料（未提供。提供時に所在を明示する）
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/02-qa-to-studio.md
