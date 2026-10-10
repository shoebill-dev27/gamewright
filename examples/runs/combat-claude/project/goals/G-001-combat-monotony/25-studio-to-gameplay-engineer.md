---
kind: handoff
goal: G-001
seq: 25
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 25: studio → gameplay-engineer — 変更内容の記述に波の条件の規則を 1 文足して Build を確定する

## Task

Build の変更内容の記述(Handoff 22 の 2.1〜2.4)に、決まった波の条件の規則を足して確定させる。D-008 により、変更内容を正確に書いた時点で Build 完了とする。コードの実装はない。

## Context

G-001(戦闘の単調さ)。Build(6e)は、波 2 以降の条件(K、T)を調べ始める時点が仕様に未定義だったため `question` で返った。`game-designer` が規則を決め(D-009)、`design/combat.md` を更新した。残るのは記述への反映だけで、これで Build が確定する。

## Findings

**決まった規則(D-009、`game-designer` の決定。変更しない)**

- 波 N の次の波の K と T は、波 N の全員が出現中に入った時点から調べ始める。それより前は判定も計測もしない。
- 出現位置の待ち(プレイヤーがスロットから 4 タイル未満、最大 2.0 s)の敵は「生きている敵」に数えない。出現中に入った時点から数える。出現中の敵を数える既存の規則(D-005)は変わらない。
- T の起点は仕様のまま(最後の敵の出現中が終わった時点)。
- 全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波が出る。そうでなければ、K 体以下になるか T s たつかの先に起きた方。
- 待ちがない波は従来どおり(出現を決めた時点が調べ始める時点)。
- 複数の敵が同じ波で待つ場合は、スロットごとに別々に待ち、同時に始まる。全員が出現中に入るまで次の波の判定は始まらない。
- 待ちの間にプレイヤーが動いてスロットから 4 タイル以上になった場合、そのスロットの待ちはその時点で終わり出現中に入る。いったん終わったスロットは待ち直さない。
- 「遠い方」のスロット選びは D-005 のとおり出現を決める時点で固定。変更なし。
- 部屋の構成、K、T、出現中 0.8 s、待ち 4 タイル / 2.0 s の数値は変更なし。入力・プレイヤー側の数値も変更なし。

**記述 2.1 に足す文(`game-designer` の案)**

「波の条件(K、T)は、前の波の全員が出現中に入った時点から調べ始め、出現位置の待ちの敵は生きている敵に数えない。T の起点は最後の敵の出現中の終わり。」

**確認してほしい点**

- 上の規則を、スポナーの状態(`sim/repo-notes.md` に書かれた範囲)とどう対応づけるかを記述に書く。生きている敵の数え方、待ちの敵の扱い、調べ始める時点の持ち方を、台帳の該当項目に照らして確認し、答えのない部分は「模擬上の前提」と明記する。実コードで確認済みとは書かない。
- 規則が V7(部屋 2 の波 2)と V12(a)〜(d)の期待する挙動を満たすか、記述の上で追って確かめる。

## Decisions already made

- D-001〜D-006、D-007(台帳の進め方)。
- D-008: Build は変更内容の記述の完了で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- 規則は決めない。曖昧さや矛盾、足りない場合があれば `outcome: question` で返す(Skill どおり)。
- 新しい入力ボタンなし。プレイヤー側の数値、仕様の数値は変えない。
- 欠陥 D の原因を推測して書かない。

## Open questions

None

## Expected output

- Handoff 26(`to: studio`、`outcome: done`、stage: Build)。Studio が Verify の Handoff を `qa` と `art-director` 向けに組み直すため、`to: studio` とする。
- Findings に、確定した変更内容の全体(2.1〜2.4。2.1 に上の 1 文を統合したもの)を、客観的な記述として自己完結する形で書く。Handoff 22 を読まなくても分かること。
- 自己評価、確信度、疑いは `## Sender assessment` にだけ書く(`qa` には渡されない)。
- 台帳のうち模擬上の前提として残る項目を、Findings に一覧する(シミュレーターと Verify が前提の範囲を知るため)。

## Sender assessment

Studio の自己評価: 規則は D-009 で確定済み、足すのは 1 文と対応づけの確認のみで、新しい決定は不要と見ている。Handoff 22 の Sender assessment は転記していない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md(§4.1、§4.3、V7、V12)、sim/repo-notes.md
- Decisions: decisions/D-009-wave-condition-start-and-waiting-enemies.md, decisions/D-005-flinch-contact-and-far-slot-rules.md, decisions/D-008-owner-simulated-build-judgment.md, decisions/D-007-build-without-code-access-assumption-register.md
- Previous handoff: goals/G-001-combat-monotony/24-game-designer-to-studio.md
