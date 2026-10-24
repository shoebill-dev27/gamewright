---
kind: handoff
goal: G-001
seq: 23
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 23: studio → game-designer — 波 2 以降の条件を調べ始める時点の欠落を埋める(+ §10 の参照追記)

## Task

(1) `design/combat.md` §4.1 の「次の波の条件(K / T)をいつから調べ始めるか、出現位置の待ちの敵を『生きている敵』に数えるか」を決めて仕様に書く。(2) 小さな追記として、§10 に `design/grub-charge-telegraph.md` への参照を足す。

## Context

G-001(戦闘の単調さ)。方向は D-002、規則は D-003・D-005 で決まり、Build は `gameplay-engineer` が変更内容の記述として進めている(D-008: 記述の完了で Build 完了、以後の Verify・Play・Review は記述から作る模擬ビルドに基づく)。記述を書く途中で、仕様が定義していない場合が 1 つ見つかり、Build がその部分だけ止まっている。それ以外の変更内容は書き上がっている。

## Findings

**(1) 欠落している場合(客観的な事実)**

- §4.1 は、波 2 以降を「生きている敵が K 体以下(出現中の敵を含む)、または前の波の最後の敵の出現中が終わってから T s の、先に起きた方」で出すと定めている。
- 出現は、スロットごとに、プレイヤーとスロット座標の距離が 4 タイル未満なら待つ(最大 2.0 s)。待ちが終わると、そのスロットの敵が出現中(0.8 s)に入る。
- 待ちの間の敵が「生きている敵」に含まれるか、K と T をいつから調べ始めるかは、仕様に書かれていない。文面どおりに読むと、次のことが起きうる。
  - 部屋 2: 波 1 は突進型 1 体、K=0。その敵が出現位置の待ちに入ると、生きている敵が 0 体になり、波 2 がすぐ出る。
  - 部屋 1: 波 1 は通常 Grub 2 体(L, R)、K=1。片方だけが待つと、生きている敵が 1 体になり、波 2 が早く出る。
- 関係するのは、部屋 1〜5 の波 1 → 波 2 の切り替えで、波 1 のどれかの敵が待ちに入る場合。待ちが起きるのは、プレイヤーが出現位置から 4 タイル未満のときだけ。
- 部屋ごとの値(§4.3): 部屋 1 K=1, T=10 s / 部屋 2 K=0, T=15 s / 部屋 3 K=1, T=12 s / 部屋 4 K=1, T=12 s / 部屋 5 K=1, T=12 s。

**選択肢と技術的な費用**(どれもスポナーの 1 か所の判定で、費用は小さい)

- A: 前の波の全員が出現中に入った時点から K と T を調べ始める。待ちの敵は「生きている敵」に数えない。T の起点は仕様の定義(最後の敵の出現中の終わり)のまま。
- B: 待ちの敵を「生きている敵」に数える。調べ始める時点は、前の波の出現が決まった時点。
- C: 設計側が別の規則を決める。

実装側(`gameplay-engineer`)は、仕様の他の文(「すべての波が出現し」、T の起点の定義)と整合し、検証が単純になる点から A を提案している。決めるのは `game-designer` である。

**(2) §10 の追記(小さな作業)**

`design/grub-charge-telegraph.md`(D-006)が作られたが、`design/combat.md` §10 からの参照がない。§10 に、突進の予告の見た目の詳細はそのファイルにある旨を 1 行で足す。戦闘の規則や数値は変えない。

## Decisions already made

- D-001: 攻撃とダッシュのワンボタン戦闘。新ボタンなし。
- D-002: 主軸は部屋の構成と進行。併用は予告つき Grub 突進の 1 つ。
- D-003: 突進は同時 1 体、方向固定、予告中は無害。部屋は突進スイッチで外せる。
- D-005: 突進型は 3 状態で怯まない。接触は突進ごとに最初の重なりで 1 回。「遠い方」は出現を決める時点で選ぶ。

## Constraints

- 部屋の構成、K・T の値、出現中 0.8 s、待ちの 4 タイル / 2.0 s、その他の数値は変えない(この欠落を埋めるのに必要なら、理由を書く)。
- 新しい入力ボタン、プレイヤー側の数値、キットは変えない(D-001)。
- 答えは、受け入れ基準(V7 など)を、プレイヤーに見える挙動で検証できる形にする。
- 規則が D-002・D-003 の変更、スコープや方向の変更を要する場合は決めず、`outcome: question` で返す(Studio が `game-director` に回す)。

## Open questions

- 波 2 以降の K と T を、いつから調べ始めるか。待ちの敵を「生きている敵」に数えるか。
- 上記で、複数の敵が同じ波で待つ場合、プレイヤーが待ちの間に動いて距離が 4 タイル以上になった場合の扱いに追加の規則が要るか(要らなければ「不要」と書く)。

## Expected output

1. `design/combat.md` §4.1 に決めた規則を書き、V7 など影響する受け入れ基準を更新する。§10 に参照を 1 行追記する。
2. 選択肢のうち採らなかったものがあり、この規則が当該ステップを越えて効くため、Decision(`decisions/D-009-...md`)を記録する。
3. 結果を `goals/G-001-combat-monotony/24-game-designer-to-studio.md` に Handoff(`to: studio`、`outcome: done`)として書く。Studio が `gameplay-engineer` に戻す(記述に 1 文を足して Build を完了する)。実装側の情報(Sender assessment)は求めない。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md(§4 と §10)、design/grub-charge-telegraph.md、project.md#constraints
- Decisions: decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-005-flinch-contact-and-far-slot-rules.md
- Previous handoff: none
