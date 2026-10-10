---
kind: handoff
goal: G-001
seq: 24
from: game-designer
to: studio
stage: Design
outcome: done
---
# 24: game-designer → studio — 波 2 以降の条件を調べ始める時点を決めた(案 A、D-009)+ §10 の参照追記

## Task

Studio は、この Handoff を `gameplay-engineer` に戻す。`gameplay-engineer` は、変更内容の記述に下記の 1 文を足して Build を完了する(D-008)。

## Context

G-001(戦闘の単調さ)。Handoff 23 の依頼に応える。波 2 以降の K と T をいつから調べ始めるか、出現位置の待ちの敵を「生きている敵」に数えるかが仕様になかった。Build はその部分だけ止まっていた。

## Findings

**(1) 決めた規則(案 A、D-009)**

- 波 N の次の波の K と T は、波 N の全員が出現中に入った時点から調べ始める。それより前は判定も計測もしない。
- 出現位置の待ち(プレイヤーがスロットから 4 タイル未満、最大 2.0 s)の敵は、「生きている敵」に数えない。出現中に入った時点から数える。出現中の敵を数える既存の規則(D-005)は変わらない。
- T の起点は仕様のまま(最後の敵の出現中が終わった時点)。
- 全員が出現中に入った時点で生きている敵が K 体以下なら、すぐ次の波が出る。そうでなければ、K 体以下になるか T s たつかの先に起きた方。
- 待ちがない波は従来どおり(出現を決めた時点が調べ始める時点)。
- 数値は何も変えていない。

**`gameplay-engineer` が記述に足す 1 文の案**: 「波の条件(K、T)は、前の波の全員が出現中に入った時点から調べ始め、出現位置の待ちの敵は生きている敵に数えない。T の起点は最後の敵の出現中の終わり。」

**(2) Open questions への答え**

- 複数の敵が同じ波で待つ場合: スロットごとに別々に待ち、同じ波の待ちは同時に始まる。全員が出現中に入るまで次の波の判定は始まらない。追加の規則は**不要**(§4.1 に明記した)。
- 待ちの間にプレイヤーが動いて 4 タイル以上になった場合: そのスロットの待ちはその時点で終わり、出現中に入る(2.0 s を待ち切らない)。いったん終わったスロットは待ち直さない。既存の文面の明記で、新しい数値や規則は足していない。
- 「遠い方」のスロット選びは、D-005 のとおり出現を決める時点で固定する。変更なし。

**(3) 更新した文書**

- `design/combat.md`: §4.1 に規則を追記、§4.3 の表の注、V7 の更新、V12 の追加(部屋 2 と部屋 1 の例を、プレイヤーに見える挙動で検証できる形にした)、§6.2 に体験の観点を 1 つ追加、§8 と §9 に参照を追記、変更履歴の更新。
- `design/combat.md` §10: `design/grub-charge-telegraph.md`(D-006)への参照を 1 行足した。戦闘の規則や数値は変えていない。
- `decisions/D-009-wave-condition-start-and-waiting-enemies.md`: 案 B(採らなかった)と案 C を理由とともに記録した。

**(4) 数値と制約**

部屋の構成、K、T、出現中 0.8 s、待ち 4 タイル / 2.0 s は変えていない。新しい入力ボタン、プレイヤー側の数値は変えていない(D-001)。D-002、D-003 の変更もスコープの変更も要らないので、`question` ではなく `done` とした。

## Decisions already made

- D-001、D-002、D-003、D-005。
- D-009(新規): 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- 受け入れ基準は V7 と V12。Verify は、記述から作る模擬ビルド(D-008)に対して V12 の (a)〜(d) を確認する。

## Open questions

None

## Expected output

Studio は `gameplay-engineer` に戻す。`gameplay-engineer` は記述に 1 文を足し、Build を完了する。その後の Verify は V7 と V12 を含めて行う。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md(§4.1、§4.3、V7、V12)
- Decisions: decisions/D-009-wave-condition-start-and-waiting-enemies.md, decisions/D-005-flinch-contact-and-far-slot-rules.md
- Previous handoff: goals/G-001-combat-monotony/23-studio-to-game-designer.md
