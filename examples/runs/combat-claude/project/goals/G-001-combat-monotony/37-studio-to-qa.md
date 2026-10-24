---
kind: handoff
goal: G-001
seq: 37
from: studio
to: qa
stage: Verify
outcome: routed
---
# 37: studio → qa — 模擬ビルド 0.6 の再確認(V7 の「同距離のとき」の規則だけ)

## Task

模擬ビルド `sim/build-0.6.md` が、仕様の基準 V7 のうち「遠い方のスロットを選ぶとき、2 つの距離が同じ場合の規則」を満たすか確認する。あわせて、他の基準(V1〜V12)の記述が前回の確認から崩れていないかを、ビルドの記述の範囲で確認する。

## Context

G-001(戦闘の単調さの改善)。D-008 により、結果はすべて模擬ビルドの記述に基づく。実機の証拠ではない。前回の再検証(Handoff 34)では、V7 の「同距離のとき」の規則だけが、ビルドの記述の用語のために仕様の意図と一致するか確認できず、pass にできなかった。それ以外は pass(模擬)だった。今回はその 1 点の再確認が中心である。

## Findings

期待値(仕様 `design/combat.md` §4.1 と D-005 から導かれる内容。仕様の文面が優先):

- 「FL / FR のうち、プレイヤーから遠い方」を選ぶ波(部屋 3 の波 2、部屋 5 の波 2)では、その波の出現を決める時点のプレイヤーの位置を使い、プレイヤーの中心から FL と FR の各スロットの中心までの距離を比べ、大きい方を選ぶ。
- 2 つの距離が同じ場合は FL(奥の左隅 = far-left corner)を選ぶ。FR を選ばない。
- 選ぶ対象は奥の左隅(FL)と奥の右隅(FR)の 2 つだけで、手前(扉側)の角に当たるスロットは存在しない。
- 選んだあと、待ちの間にプレイヤーが動いても選び直さない。

確認の観点:

1. ビルドの記述が、同距離のとき FL を選ぶと一意に読めるか。他の箇所の far-left / far-right などの用語と食い違わず、仕様の FL(奥の左隅)を指すと確認できるか。
2. 記述が別の用語(例: 手前の角を指す語)や別のスロットを示している場合は、その箇所を原文のまま引用して報告する。仕様と一致するかを推測で補わない。
3. V7 の他の部分(Grub 速度ほか)と V1〜V12 は、前回から記述が変わっていないか確認する。F-1、V10、V12(c) は前回 pass(模擬)で、再確認は不要。ただし記述が前回と食い違っている場合は報告する。

## Decisions already made

- D-005: 「遠い方」は出現を決める時点で選ぶ。同距離は FL。
- D-008: 結果は模擬ビルドに基づく。結果に模擬であることを明記する。
- D-009: 波の条件を調べ始める時点と待ちの敵の扱い(変更なし)。

## Constraints

- 基準は `design/combat.md` の V7 と、仕様の該当節。ビルドの記述を読んで判定する。実装者の説明は渡されていない。ビルドを書いた側の意図を推測しない。
- 欠陥 D(被弾直後のダッシュ中のダメージ)は範囲外。観察として気づいた場合は、判定に入れず分けて記録する。
- 仕様にない期待値を作らない。仕様が未定義なら `question` で返す。
- Sender assessment は含まれない。

## Open questions

- なし(ビルドの記述が読めない、または仕様と矛盾して判定できない場合は、その事実を報告する)。

## Expected output

V7 の同距離の規則と、確認した他の基準ごとの結果(pass / fail / 確認不能)を、根拠となるビルドの記述の引用つきで報告する。すべて模擬ビルドに基づく旨を書く。`to: studio`(Play の Handoff を Studio が実装の履歴なしで組むため)。`outcome` は pass / fail / question のいずれか。V7 の同距離の規則が再び確認不能または不一致の場合は、その事実を引用つきで報告する。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md(V7、§4.1)、sim/build-0.6.md、project.md#constraints
- Decisions: decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/34-qa-to-studio.md
