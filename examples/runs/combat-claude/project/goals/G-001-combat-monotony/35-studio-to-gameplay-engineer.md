---
kind: handoff
goal: G-001
seq: 35
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 35: studio → gameplay-engineer — 変更内容 2.1 の「同距離のとき」の規則の用語を、仕様の FL に合わせて明記する

## Task

変更内容 2.1〜2.4 のうち、「遠い方のスロットを選ぶ」規則の同距離のときの記述を確認し、仕様の用語(奥の左隅 = far-left corner、略称 FL)で曖昧さなく書き直す。修正後の変更内容 2.1〜2.4 の全体を自己完結で返す。

## Context

G-001(戦闘の単調さの改善)。D-008 により、Build は変更内容の記述で完了とし、模擬ビルドはランタイムのシミュレーターがその記述から作る。判定は模擬ビルドに基づく。

前回の再検証(Handoff 34、`qa`、模擬ビルド `sim/build-0.5.md`)では、F-1、V10、V12(c) が解消し、V7 の Grub 速度、中心間の距離、出現を決める時点で選ぶこと、選び直さないことも仕様と一致した。残ったのは 1 点だけ: V7 の「同距離のとき」の規則の用語。

## Findings

(`qa` の報告 Handoff 34 の客観的な内容。実装の説明ではない。)

- 仕様(`design/combat.md`、D-005)の規則: 「遠い方」は、プレイヤーの中心から各スロットの中心までの距離で比べる。波を出す時点で選び、待ちの間に選び直さない。**完全に同じ距離のときは FL(奥の左隅)を使う。**
- `sim/build-0.5.md` の該当箇所は「完全に同じ距離なら front-left corner を使う」と書いている。同じビルドは部屋 4 の記述では同じスロットを「far-left corner」と呼んでおり、同距離の規則だけが「front-left」になっている。
- `qa` は、「front-left」が FL(奥の左隅)の略か、別の角(字面どおりなら選択の対象ではない手前の角)かをビルドの記述から決められず、V7 の同距離の部分を pass にできなかった。推測で pass にはしていない。
- 期待値は仕様で定義済みで、Design に回す問題ではない。直すのは記述の用語である。
- 他の基準(V1〜V6、V8〜V12、およびV7 の他の部分)は pass(模擬)で、変えてはならない。

## Decisions already made

- D-005: 「遠い方」の規則(同距離は FL)。
- D-008: Build は変更内容の記述で完了。模擬ビルドはシミュレーターが作る。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い(変更しない)。

## Constraints

- 数値、規則、入力は変えない。直すのは同距離の規則の用語と、それに伴う表記の統一だけ。新しい入力ボタンなし(D-001)。
- 欠陥 D(被弾直後のダッシュ中にダメージ)は範囲外。原因の推測も、規則の変更も書かない。
- 変更内容 2.1〜2.4 は Handoff 32 の記述を元にし、修正後の全体を自己完結で書く(「前と同じ」「Handoff 32 を参照」で済ませない)。
- 仕様と食い違う、または仕様に欠けている点があれば、自分で決めず `outcome: question` で返す。
- 模擬ビルドを自分で編集しない。

## Open questions

1. Handoff 32 の変更内容は、同距離の規則をどう書いていたか。「FL(奥の左隅)」と書いていた場合は、シミュレーターが記述を写す過程で用語が変わった可能性がある。その事実だけを報告する(原因は決めつけない)。「front-left」と書いていた場合は、仕様と違うので FL に直す。
2. 変更内容の中に、方角の用語が仕様と揺れている箇所が他にないか(far-left / far-right / FL / FR の表記)。あれば統一する。

## Expected output

- `to: studio`、`outcome: done`。
- Findings に、修正後の変更内容 2.1〜2.4 の全体を自己完結で書く。同距離の規則は、「プレイヤーの中心から各スロットの中心までの距離が完全に同じなら、奥の左隅(far-left corner、FL)を使う。手前の角ではない」のように、角の呼び名と意味が一意に読める文にする。図や座標の対応が仕様にあれば、それに合わせた表記にする。
- Open questions 1 と 2 の答えを客観的な事実として書く。
- 自己評価は Sender assessment にだけ書く(`qa` には渡さない)。
- 結果は Studio が、`qa` の再検証(V7 の同距離の規則だけ)の Handoff に、実装の説明なしで組み直す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md(§4 の「遠い方」と同距離の規則)、sim/repo-notes.md、sim/build-0.5.md(参照のみ。シミュレーターの出力で、編集しない)
- Decisions: decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/34-qa-to-studio.md(修正前の変更内容は goals/G-001-combat-monotony/32-gameplay-engineer-to-studio.md)
