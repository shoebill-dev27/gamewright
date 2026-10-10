---
kind: handoff
goal: G-001
seq: 1
from: studio
to: qa
stage: Observe
outcome: routed
---
# 01: studio → qa — ダッシュ中の被ダメージを再現する

## Task

Owner の報告を模擬ビルドで再現し、戦闘仕様と照合して、再現手順・期待挙動・実際の挙動・受け入れ条件を備えた不具合報告を作成する。再現できない場合や仕様が不足する場合は、その不足を明示して Studio に返す。

## Context

Owner の依頼：

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

対象は Lantern Depths の build 0.3。短時間のトップダウン型アクション roguelite で、現在は 5 部屋、敵 2 種、攻撃とダッシュの構成。dry-run のため、ビルドを実行する代わりに `sim/build-0.3.md` を読む。

## Findings

- Owner は再現可能と述べているが、具体的な手順・タイミング・敵の種類は未提示。
- 独立した再現確認はまだない。
- `design/combat.md` にダメージと無敵の規則がある。Studio は本文を受け取っておらず、期待挙動を確定していない。
- 原因や修正方法は未判断。

## Decisions already made

この Goal での Decision はなし。

Project Context では、既存の D-001 により攻撃とダッシュを基本とし、攻撃・ダッシュ・ポーズ以外の入力追加には Owner 承認が必要とされている。本段階は既存挙動の観察のみを行う。

## Constraints

- 実在のゲーム repository はない。模擬ビルドから確認できたことと、確認できないことを区別する。
- Desktop、キーボード・ゲームパッド、30 / 60 FPS が対象。模擬資料に情報がない条件を検証済みとしない。
- ダッシュ全体が無敵であるとは仮定せず、既存仕様を根拠に期待挙動を定める。
- 実装、ルール変更、技術方式の決定は行わない。
- QA は独立した新しい executor で実行し、実装者の説明・自己評価は受け取らない。

## Open questions

- どの手順・条件で被ダメージが発生するか。
- 発生時点は仕様上の無敵区間に含まれるか。
- 期待挙動と実際の挙動に差があるか。
- 入力方式や FPS による差が資料から確認できるか。
- 既存仕様から、修正の受け入れ条件を十分に定義できるか。

## Expected output

次の Handoff を `to: studio` として作成し、Findings に以下を記載する。

- 参照した仕様と観察の根拠。
- 再現手順、条件、期待挙動、実際の挙動、再現性、重大度。
- 不具合が確認できた場合、既存仕様に基づくプレイヤーから観察可能な受け入れ条件。
- 未確認の環境・条件と、追加で必要な情報。

再現報告が完成した場合は `outcome: done`、情報不足・期待挙動の未定義・報告と仕様の一致などで修正へ進めない場合は `outcome: question` とする。Studio が結果を受けて次の段階を確定する。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Decisions: none
- Previous handoff: none
