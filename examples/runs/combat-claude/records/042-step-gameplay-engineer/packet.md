# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/35-studio-to-gameplay-engineer.md
next_seq: 36

## You may write

- goals/G-001-combat-monotony/36-gameplay-engineer-to-<recipient>.md

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/35-studio-to-gameplay-engineer.md
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
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3 → G-001 仕様、暫定)

状態: G-001 / D-002 / D-003 / D-005 / D-009 に基づく仕様。**この文書の新しい数値はすべて暫定値(P)**。H1〜H4(ゲームパッドの操作感、各部屋の実時間、音と演出、敵の速度と弾速など)の実機確認後に調整する。確認前に、プレイヤー側の数値は変えない。

変更履歴: Handoff 10 / D-005 で、怯み(§2.1、§8)、接触の定義(§3.4、§3.5、V3、V4、V11)、遠い方のスロットの規則(§4.1、§4.3)、波の既定(§4.1)を明記した。数値は変えていない。
Handoff 24 / D-009 で、波 2 以降の K と T を調べ始める時点と、出現位置の待ちの敵の扱い(§4.1)を明記し、V7 を更新し、V12 を足した。§10 に `design/grub-charge-telegraph.md` への参照を足した。数値は変えていない。

## 0. 表記と共通ルール

- 長さは秒(s)、距離はタイル、速度はタイル/秒で書く。フレーム数では定義しない。
- 対応する条件は 30 FPS と 60 FPS。タイマーはゲーム内の経過時間で進める。ポーズ中は止まる。
- 30 FPS と 60 FPS で、各状態の長さの差は 30 FPS の 1 フレーム(約 0.034 s)以内にする。接触が起きるかどうかも、FPS によって変わらないこと。
- ビルドの既存値を使う項目は「既存」と書く。
- 暫定値には `(P)` を付ける。

## 1. Player kit(変更なし)

- **Attack**(ボタン1つ): 向いている方向への短い振り。1 ダメージ。回復 0.35 s。
- **Dash**: 0.25 s で 4 タイル。ダッシュ中はずっと無敵。クールダウン 0.6 s。ダッシュ中に押した攻撃は予約され、ダッシュ終了時に出る。
- **被弾**: 1 ハートのダメージ。0.3 s の硬直(入力不可)。被弾から 0.8 s 後まで無敵。

この仕様はプレイヤー側の数値を一切変えない。

## 2. 敵

| 敵 | HP | 挙動 |
|---|---|---|
| Grub(通常型) | 2 | プレイヤーへまっすぐ歩き、接触で噛む(1 ダメージ)。予告なし。 |
| Grub(突進型) | 2 | 歩いて近づき、条件がそろうと予告つきで突進する(§3)。それ以外は通常型と同じ。 |
| Spitter | 2 | 固定位置。一定間隔で、プレイヤーに向けて遅い弾を撃つ。 |

### 2.1 共通ルール

- **出現中(spawn-in)**: 敵は出現位置に 0.8 s(P)の間「出現中」で現れる。この間は行動せず、ダメージも受けず与えない。出現中だと見えることが必須(柱3)。見た目は art-director が決める。
- **弾**(Spitter):
  - 速度 4.0 タイル/s(P)。ダメージ 1 ハート(P)。
  - 撃った瞬間のプレイヤーの位置へ直進する。先読みはしない。
  - 壁で消える。敵の体は通り抜け、敵にダメージを与えない。
- **敵どうし**: 歩くときの敵どうしの押し合いは既存のまま(未定義のまま)。突進中の Grub は他の敵の体を通り抜け、ダメージを与えない。
- **敵の被ダメージと怯み(Flinch)**:
  - 既存の 0.2 s の怯み(被弾すると行動を中断して Chase に戻る)は、**Chase など通常の状態でだけ**起きる。通常型 Grub と Spitter の怯みは既存のまま変えない。
  - **突進型 Grub の Windup、Charge、Recovery の間は怯まない**。攻撃を受けてもダメージ(HP)だけ受け、状態、方向、残り時間は変わらない。ノックバックが既存にある場合も、この 3 つの状態の間は受けない(位置を動かされない)。
  - 出現中の敵は、ダメージも怯みも受けない(上の「出現中」のとおり)。出現中が終わった後は上の規則に従う。
  - HP が 0 になれば、どの状態でもその時点で倒れる。
  - 突進型 Grub が Chase 中に怯んだ場合は、Chase に戻るだけ。開始条件(§3.3)のタイマーは怯みで巻き戻さない。

### 2.2 Spitter の数値(部屋ごと、§4 の表)

- 撃つ間隔は部屋ごとに変える。出現中が終わってから最初の 1 発までは 1.0 s(P)。
- 撃ち方(直進、1 発ずつ、先読みなし)は変えない。

## 3. Grub 突進

### 3.1 意図

Grub が立ち止まって溜め、その直線上に突っ込む。プレイヤーは予告を見て「横に出る」「ダッシュの無敵で突進を抜ける」を選ぶ。抜けたあとの隙に反撃できる。害を与える前に、必ず予告が見える(柱3)。

### 3.2 状態

| 状態 | 長さ | 動き | 接触ダメージ | 怯み |
|---|---|---|---|---|
| Chase | 条件まで | 部屋の Grub 速度で歩く | あり(1 ハート) | 既存(0.2 s) |
| Windup(予告) | **0.7 s (P)** | その場で停止。突進方向を **Windup の開始時に固定** | **なし** | **なし** |
| Charge | 距離 7.0 タイルまたは壁まで | 固定した方向へ **8.0 タイル/s (P)** で直進(最大約 0.875 s) | あり(1 ハート。§3.4 の接触の定義による) | **なし** |
| Recovery(隙) | **0.8 s (P)** | その場で停止 | **なし** | **なし** |

Recovery が終わったら Chase に戻る。

### 3.3 開始条件(Chase → Windup)

次をすべて満たしたとき。

1. 出現中が終わってから 1.5 s(P)以上たっている。前回の Recovery が終わってから 2.5 s(P)以上たっている。
2. プレイヤーとの距離(中心間)が 3.0〜6.0 タイル(P)。
3. 部屋の突進スイッチがオンで、その Grub が突進型。
4. **別の突進型 Grub が Windup または Charge 中でない**(同時に予告できるのは 1 体まで)。

### 3.4 規則

- **方向の固定**: Windup の開始時に、そのときのプレイヤーの位置へ向く。その後プレイヤーが動いても方向は変わらない。直線上を走る範囲が「突進の線」。幅は Grub の既存の接触判定が通る範囲(新しい大きさは決めない)。
- **予告の条件**:
  - Windup の 0.7 s の間ずっと見えている。
  - これから突進すること、およびその方向がわかる。
  - 通常の Grub の歩きと見分けがつく。
  - 色だけに頼らない。音だけにも頼らない。
- **接触の定義(D-005)**: Charge 中の接触は「**1 回の突進につき、Grub の体とプレイヤーが最初に重なった瞬間に 1 回だけ解決する**」。
  - 「最初に重なった瞬間」を、この文書では**接触の瞬間**と呼ぶ。更新ごとのスイープ判定で求め、FPS によって有無が変わらない。Charge の開始時にすでに重なっている場合は、Charge の開始の瞬間を接触の瞬間とする(Windup と Recovery の間の重なりは無害で、数えない)。
  - 接触の瞬間にプレイヤーが**無敵**(ダッシュ中、被弾後の 0.8 s)なら、ダメージなし。Grub は通り抜けて走り続ける。**その突進は、その後に重なりが続いても、無敵が切れても、もうダメージを与えない**。
  - 接触の瞬間にプレイヤーが無敵でなければ、**1 ハートのダメージを 1 回だけ**与える。その突進は、その後もうダメージを与えない。
  - 1 回の突進で与えるダメージは 1 回まで。次の突進では、また最初の重なりから数える。
  - Chase 中の噛みつきは、この規則に含めない(既存のまま)。
- **終了**: 7.0 タイル進むか壁に当たったら Charge が終わり、すぐ Recovery に入る。壁に当たったときの特別な処理はない。
- **Windup 中に倒された場合**: 予告はその場で消え、同時予告の枠が空く。Charge 中に倒されたときも同じ。Windup 中の攻撃はダメージを与えるが、Windup は中断されない(怯まない、§2.1)。HP が 0 になれば倒れる。
- **ポーズ**: 状態の時間は止まる。

### 3.5 ダッシュの無敵で抜けられるか(確認)

- 止まっているプレイヤーに対して、Windup の開始時の距離が d タイルなら、接触の瞬間は Windup の開始から約 0.7 + (d − 接触までの余白)/8 s 後。余白を無視すると、おおよそ 0.7 + d/8 s。
  - d = 3 で約 1.075 s、d = 6 で約 1.45 s。
- ダッシュの無敵は 0.25 s なので、**接触の瞬間の 0.25 s 前から接触の瞬間までに、ダッシュを始めれば抜けられる**。窓の幅は 0.25 s(30 FPS で約 7〜8 フレーム)。
- 接触は最初の重なりで 1 回だけ解決する(§3.4)ので、窓は重なりの長さに削られない。ダッシュが重なりの途中で終わっても、その突進はダメージを与えない。窓の数値は変えない(0.25 s のまま)。
  - 根拠: 窓が 0.25 s あれば、読んでから押す操作として成り立つ見込みがあるため。実機で「ダッシュが使える」と感じられるかは H1 とあわせて Play で確認し、足りなければ §7 の調整項目で扱う。窓を重なりの長さ(約 0.1〜0.2 s)ぶん狭くする案 B は採らない(D-005)。
- 横方向のダッシュなら線から出るので、窓はこれより広い。
- 連続する 2 回の突進のあいだ: 次の Windup は前の Charge が終わってから始まる。次の接触は前の接触の約 1.2 s 以上あと(d = 6 の最悪の場合)。ダッシュのクールダウンが「ダッシュの終了から 0.6 s」と読んだ最悪の場合でも、前の接触から約 0.85 s 後に再使用できる。**ダッシュが間に合わない並びは作られない。**
- 歩いて線から出られるかは、プレイヤーの移動速度(未定義)に依存する。この仕様では保証しない。歩きだけで簡単に避けられ、ダッシュを使う理由が出ない場合は §7 の調整項目で調整する(C の検証)。
- 被弾直後(0.8 s 以内)にダッシュを始めた場合の窓は、この確認に含めない。欠陥 D(§8)の再現結果が出るまで、規則を書かない。

### 3.6 反撃の隙

Recovery(0.8 s)は止まっていて接触ダメージもない。攻撃の回復 0.35 s なら、隣接していれば 2 回振れる(Grub の HP 2)。怯まないので、1 回目の攻撃で Recovery が中断されることはない。ただし、攻撃の届く距離は未定義なので、2 回当てられる位置取りが実機で成立するかは Play で確認する。

## 4. 部屋の進行

### 4.1 共通ルール

- 部屋の総数は 5、各部屋の敵の数は 3〜6 体のまま(既存)。
- 波(wave):
  - 次の波は、「生きている敵が K 体以下」または「前の波の出現中が終わってから T s」の、先に起きた方で出現する。
  - 「前の波の出現中が終わってから T s」の起点は、**その波の最後の敵の出現中が終わった時点**(出現位置の待ちがあれば、その待ちが終わって出現中も終わった時点)。
  - 「生きている敵」には**出現中の敵を含める**。
  - 部屋は、すべての波が出現し、すべての敵が倒れたときに終わる。
- **次の波の条件を調べ始める時点(D-009)**:
  - 波 N の次の波(N+1)の K と T は、**波 N の全員が出現中に入った時点**から調べ始める。それより前は、K の判定も T の計測もしない。
  - 波 N に出現位置の待ち(下記)に入っている敵がいる間は、その敵は「生きている敵」に**数えない**(まだ出現していない。出現位置に敵は存在せず、攻撃も当たらない)。待ちが終わって出現中に入った敵から、数える。
  - 波 N の全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波を出す。そうでなければ、K 体以下になるか、T s たつかの先に起きた方で出す。T の起点は上のとおり(最後の敵の出現中が終わった時点)で、変わらない。
  - 波 N に待ちの敵がいなければ、波 N の出現を決めた時点が、そのまま調べ始める時点になる(従来どおり)。
- 出現位置(スロット): 扉側(Door)、奥(Far)、左側面(L)、右側面(R)、奥の左隅(FL)、奥の右隅(FR)。実際の座標は部屋データ。
  - 出現の時点でプレイヤーがスロットから 4 タイル未満なら、出現を最大 2.0 s 待つ。2.0 s たったら、そのまま出現中に入る。
  - 待ちはスロットごとに別々に数える。同じ波の複数のスロットの待ちは、波の出現を決めた時点から同時に始まる。
  - 待っている間にプレイヤーが動いてスロットから 4 タイル以上になったら、そのスロットの待ちはその時点で終わり、出現中に入る(2.0 s を待ち切らない)。いったん待ちが終わったスロットは、プレイヤーが戻ってきても待ち直さない。追加の規則は不要。
  - **出現位置にプレイヤーが重なっても、押し出さない**。出現中の 0.8 s は無害で、見えるので動ける。待ちは最大 2.0 s (上のとおり)。
- **「プレイヤーから遠い方」の規則**(部屋 3 の波 2、部屋 5 の波 2 の「FL または FR」):
  - その波の出現を決める時点(出現位置の待ちを始める前)のプレイヤーの位置から、FL と FR の各スロット座標への距離(中心間)を比べ、遠い方を選ぶ。選んだあと、待ちの間にプレイヤーが動いても選び直さない。
  - 同じ距離のときは FL を選ぶ。
  - 同じ波に FL か FR が別の敵のスロットとして指定されている場合は、この規則の対象外(固定のスロットが優先)。
- **突進スイッチ**: 部屋ごとに、突進をオンまたはオフにできる。オフのとき、突進型の Grub は同じスロットの通常型 Grub に置き換わる。敵の数、波、出現位置は変わらない。

### 4.2 進行の筋

| 部屋 | 学ぶこと | 組み合わせさせること |
|---|---|---|
| 1 | Grub が来る。振る。間合い。 | なし(基本) |
| 2 | **突進の予告を読む**。ダッシュで抜ける。 | 突進と、左右からの通常型 |
| 3 | **Spitter** の線から出続ける。止まると撃たれる。 | Spitter と Grub(突進なし) |
| 4 | 突進と弾を、同時に処理する。 | 突進 + Spitter + 通常型 |
| 5 | 全部が同時に来る。波の切り替えの判断。 | 突進 2 体(順番に来る) + Spitter 複数 |

### 4.3 部屋ごとの構成

「遠い方」は §4.1 の規則による。

| 部屋 | 波 | 構成(スロット) | 次の波の条件 | Grub 速度 | Spitter 間隔 | 突進 |
|---|---|---|---|---|---|---|
| 1 | 1 | 通常 Grub × 2(L, R) | | 2.0 | – | オフ |
| | 2 | 通常 Grub × 1(Far) | K=1, T=10 s | | | |
| 2 | 1 | **突進型 Grub × 1**(Far) | | 2.0 | – | オン |
| | 2 | 通常 Grub × 2(L, R) + 突進型 Grub × 1(Far) | K=0, T=15 s | | | |
| 3 | 1 | Spitter × 1(Far) + 通常 Grub × 1(L) | | 2.2 | 2.0 s | オフ |
| | 2 | Spitter × 1(FL または FR のうち、プレイヤーから遠い方)+ 通常 Grub × 1(R) | K=1, T=12 s | | | |
| 4 | 1 | Spitter × 1(FL)+ 突進型 Grub × 1(Far)+ 通常 Grub × 1(L) | | 2.2 | 1.8 s | オン |
| | 2 | Spitter × 1(FR)+ 突進型 Grub × 1(R) | K=1, T=12 s | | | |
| 5 | 1 | Spitter × 1(Far)+ 通常 Grub × 2(L, R) | | 2.4 | 1.6 s | オン |
| | 2 | Spitter × 1(FL または FR のうち、プレイヤーから遠い方)+ 突進型 Grub × 2(L, R) | K=1, T=12 s | | | |

「次の波の条件」の行は、その波の次の波を出す条件(波 1 の全員が出現中に入った時点から調べる、§4.1)。

合計は 部屋 1: 3 体、2: 4 体、3: 4 体、4: 5 体、5: 6 体。同時に存在する敵の最大は、部屋 1: 2、2: 3、3: 3、4: 3、5: 4。

### 4.4 立って振るだけが通じなくなる理由(設計上の根拠)

- Spitter は、撃った瞬間の位置を狙う。止まっているプレイヤーには、毎回当たる(部屋 3 から)。
- 左右から同時に来る Grub は、一方向に向き直るだけでは片側を受ける(部屋 2 から)。
- 突進は、止まって見ているだけでは当たる(部屋 2、4、5)。

### 4.5 突進を外した版(部屋 2、4、5)

- 部屋 2 は、通常 Grub が 1 体、次に 3 体の部屋。部屋 1 と似るが、波と左右の挟み込みがある。この版は「案2の構成だけの効果」を見るための基準になる。
- 部屋 4 は Spitter + 通常 Grub、部屋 5 は Spitter + 通常 Grub。どれも部屋として成立する。
- 突進の効果は、突進オン/オフの比較で切り分ける。

## 5. 突進が他の脅威と同時に起きたとき(柱3)

- 同時に予告できる突進は 1 体まで。次の Windup は、前の Charge が終わってから始まる(§3.3)。
- Windup の長さは全部屋で 0.7 s に揃える。部屋ごとに変えない(読み方を一定に保つ)。
- Windup 中と Recovery 中の Grub は接触ダメージがない。「止まっている Grub は危なくない。突進に入ったら危ない」と読める。
- 弾は遅く(4.0 タイル/s)、直線で、突進の線とは別。弾が当たるタイミングは、突進の予告より遅く見える。
- 出現中(0.8 s)は、行動もダメージもない。
- 一度に見る予告は 1 つ。弾は複数ありうる。
- 突進の予告が弾で読みにくくなる場合は、§7 の順で調整する。

## 6. 検証

### 6.1 検証用(qa 向け)

各項目を 30 FPS と 60 FPS の両方で確認する。

- V1: Windup が 0.7 s(±0.034 s)。突進開始前に必ず予告が出る。予告なしの Charge はない(出現直後、Recovery 後、プレイヤーの被弾中、ポーズ復帰後を含む)。
- V2: Charge の速度が 8.0(±0.5)タイル/s。距離は 7.0 タイルまたは壁まで。方向は Windup 開始時に固定され、途中で変わらない。
- V3: 止まっているプレイヤー(d = 4)に対し、**接触の瞬間(§3.4。Grub の体との最初の重なり)の 0.25 s 前〜接触の瞬間**にダッシュを始めればダメージなし。窓から 0.05 s 外れると被弾。窓の端は FPS で 1 フレーム(30 FPS 基準)以上ずれない。ダッシュが重なりの途中で終わっても、その突進はダメージを与えない。測定は、直前 0.8 s 以内に被弾していない状態で行う(被弾直後のダッシュは欠陥 D が確認されるまで含めない)。
- V4: 接触ダメージは Chase と Charge のみ。Windup と Recovery にはない。**1 回の突進のダメージは、最初の重なりの 1 回まで**。プレイヤーが無敵のときは、ダメージなしで Grub が通り抜け、**重なりが続いても、無敵が切れても、その突進はもうダメージを与えない**。Charge の開始時にすでに重なっている場合は、開始の瞬間に 1 回解決する。次の突進では、また最初の重なりから数える。
- V5: 同時に Windup または Charge の突進型は 1 体まで。倒したら枠が空く。
- V6: 突進スイッチをオフにすると、敵の数、波、出現位置は同じで、突進が一度も起きない。
- V7: 部屋 1〜5 の波の構成、条件(K, T)、Grub 速度、Spitter 間隔が §4.3 の表と一致する。部屋 3 と 5 の波 2 の Spitter が、§4.1 の規則(出現を決める時点で遠い方、同距離は FL、待ちの間は選び直さない)で選ばれる。「T s」の起点は最後の敵の出現中の終わり、「生きている敵」には出現中の敵を含み、出現位置の待ちの敵は含まない。K と T は、前の波の全員が出現中に入った時点から調べ始める(§4.1、V12)。
- V8: 出現中が 0.8 s。この間は行動もダメージもない。出現位置にプレイヤーが重なっても押し出されず、出現中は無害。
- V9: Spitter の最初の 1 発が出現中の終了から 1.0 s、弾速 4.0 タイル/s。弾は壁で消え、敵を通り抜ける。
- V10: プレイヤー側の数値(攻撃、ダッシュ、被弾の規則)が変わっていない。
- V11: 突進型 Grub の Windup、Charge、Recovery の間に攻撃を当てると、HP は減るが、状態、方向、残り時間は変わらない(怯まない)。HP が 0 になれば、その時点で倒れる。Chase 中に攻撃を当てると 0.2 s の怯みに入り、Chase に戻る(既存)。出現中は攻撃を当ててもダメージを受けない。
- V12: 波 2 が出るタイミング(プレイヤーに見える挙動で確認する)。
  - (a) 部屋 2: プレイヤーが波 1 の突進型の出現位置(Far)から 4 タイル未満に立ち続けると、その敵は最大 2.0 s 現れない。この間、波 2 は出ない。その敵が出現中に入った時点を起点に、突進型を倒す(K=0)か、その出現中が終わってから 15 s たつかの先に起きた方で、波 2 が出る。出現中に入る前に波 2 が出ることはない。
  - (b) 部屋 1: プレイヤーが L だけ、または R だけから 4 タイル未満に立つと、そちら側の Grub は最大 2.0 s 現れず、反対側の Grub は先に出現中に入る。待つ側が出現中に入るまで、波 2 は出ない。両方が出現中に入った時点で生きている敵は 2 体(K=1 より多い)なので、1 体倒すか、最後の敵の出現中が終わってから 10 s たつかの先に起きた方で、波 2 が出る。
  - (c) 待っている間にプレイヤーが 4 タイル以上離れると、その時点で敵が出現中に入る(2.0 s を待たない)。同じ波で複数のスロットが待つ場合も、全員が出現中に入るまで波 2 は出ない。
  - (d) 待ちがない場合の波 2 のタイミングは、従来どおり(波 1 の出現を決めた時点が起点)。

### 6.2 体験の観点(Play と Review 向け)

Playtester への handoff には書かない(基準を知らせない)。

- 立って振り続けるだけでは、後半の部屋(3〜5)で被弾するか。
- 部屋ごとに、敵の出方や対応の仕方が違うと感じるか。
- 突進の予告が、害を与える前に見えて読めるか。突進に当たったとき、「予告は見えていた」と言えるか。
- ダッシュを、移動以外の戦闘の場面で自発的に使うか。使った理由を言えるか。
- ダッシュで抜けたとき、「抜けた」と感じられるか(重なったのに当たらない、あるいは抜けた直後に当たる、という違和感がないか)。
- 被弾が「自分の判断ミスのせい」と感じられるか。
- 突進中の Grub に攻撃を当てても止まらないことが、不自然に感じられないか(予告と突進が「止められない」と読めるか)。
- 30 FPS と 60 FPS で同じに感じられるか。
- 突進オンとオフを比べて、オンの方が単調さが減るか(A、C)。
- 出現位置の近くに立っていても、波 2 が理由なく早く出て敵が急に増えた、と感じないか。

## 7. 調整項目(暫定値、H1〜H4 の確認後に調整)

先に動かす順:

1. 予告が読めない場合: Windup を 0.7 → 0.9 s に伸ばす。部屋 4、5 で同時に出る数を減らす。
2. 簡単すぎる場合: 部屋 4、5 の Grub 速度、Spitter 間隔、トリガー距離。
3. 歩きだけで避けられてダッシュを使わない場合: Charge 速度(8.0 → 10.0)、Windup(0.7 → 0.55 まで)。ただし 0.5 s を下回らない。
4. ダッシュが間に合わないと感じる場合: Windup を伸ばす(項目 1)。ダッシュの窓(0.25 s)は、プレイヤー側の無敵時間そのものなので、ここでは変えない。

プレイヤー側の数値(攻撃の回復、ダッシュのクールダウンなど)は、H1 の確認後に別の判断で扱う。

## 8. 未定義のまま残す項目

- 最大ハート数: この仕様は値に依存しない。既存のビルドのまま。
- プレイヤーの移動速度、攻撃の届く距離、各敵とプレイヤーの判定の大きさ: 既存のまま。
- ダッシュのクールダウンの起点(開始か終了か): §3.5 は最悪の場合で確認済み。
- 敵どうしの歩行時の押し合い: 既存のまま、この仕様では変更しない。
- 敵の怯みとノックバック: 通常型 Grub、Spitter、突進型の Chase 中は既存のまま。突進型の Windup、Charge、Recovery は怯まない(§2.1)。
- 出現位置がプレイヤーに重なった場合: 押し出さない(§4.1)。
- 出現位置の待ちと波の条件: §4.1 で定義済み(D-009)。
- フレーム落ち(30 FPS 未満)時の挙動: サポート外。
- 欠陥 D(被弾直後のダッシュ中のダメージ)の規則: `qa` の再現結果が出てから書き足す。この仕様には含めない。V3、V4 の測定は、被弾から 0.8 s 以上たった状態で行う。
- 各部屋の実時間: H2。この仕様はラン長(15–20 分)を変えない。

## 9. 実現性の確認が要る点(technical-director 向け)

技術的な方法は決めない。次が既存のシステムで簡単にできるかを確認してほしい。

1. Grub に、歩く以外の状態(Windup、Charge、Recovery)を足せるか。接触ダメージの有効/無効を状態で切り替えられるか。
2. 突進が、速度 8.0 タイル/s、プレイヤーのダッシュ(16 タイル/s)との相対速度でも、30 FPS で接触の取りこぼしなく判定できるか。
3. 同時に予告できる突進を 1 体に制限する管理を足せるか。
4. 部屋データで、波、出現位置(スロット)、出現中(0.8 s)、Spitter 間隔、Grub 速度、部屋ごとの突進スイッチを指定できるか。
5. 既存の部屋が「3〜6 体を最初に全部出す」前提で作られていないか(波での出現に対応できるか)。
6. 敵の挙動を秒の経過時間で進めているか(フレーム数ではなく)。
7. Spitter の弾が、壁で消え、敵を通り抜ける扱いになっているか。

(1〜3 の回答は Handoff 08 にある。怯み、接触の定義、遠い方の規則は D-005 で決定済み。波の条件を調べ始める時点は D-009 で決定済み。)

## 10. art-director に渡す条件

見た目の具体案は art-director が決める。仕様として求める条件:

- **突進の予告**: Windup の 0.7 s の間ずっと見える。突進が来ることと、その方向がわかる。通常の Grub の歩きと見分けがつく。色だけに頼らない。音だけに頼らない。音を付ける場合は、Windup の開始に合わせる。
- 長さは時間(0.7 s)で決まり、30 FPS と 60 FPS で同じ長さに見える。
- Charge 中は、歩きや Windup と見分けがつく。Recovery 中は、「止まっていて攻撃が通る」とわかる。
- 突進型は Windup、Charge、Recovery の間、攻撃を受けても怯まない。攻撃が当たったことは、HP の減少が見えれば足りる(怯みの動きで示さない)。
- 突進の予告が、Spitter の弾、出現中の表示、他の敵の動きと重なっても、読める。
- 出現中(0.8 s)が、行動する敵と見分けがつく。
- 突進型の Grub が、出現時から通常型と見分けがつくかどうかは、art-director が判断する。
- 突進の予告の見た目の詳細(レーン、熾火、沈み込み、Recovery の表現など)は `design/grub-charge-telegraph.md`(D-006)にある。

## Rooms(旧記述)

旧: 5 部屋、各 3〜6 体、Grub と Spitter の混成。部屋は全敵撃破で終わる。→ §4 に置き換え。

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — lantern-depths (build 0.5)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a Playtester.

Facts carried over and still true:
- Enemies share one controller. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: a hit enemy enters a 0.2 s Flinch that interrupts anything, including Attack, then returns to Chase. Not described in `design/combat.md`.
- The player's attack is a short arc hitbox. Enemies take damage on overlap. No blocking or facing.
- Player invulnerability is one on/off flag. The dash sets it and starts a 0.25 s timer. Getting hit sets it and starts a timer ending 0.8 s after the hit. Each timer clears the flag when it ends, so a dash within 0.8 s of a hit loses protection mid-dash. This code was not touched. Other player numbers (attack damage 1, recovery 0.35 s; dash 4 tiles in 0.25 s, cooldown 0.6 s, buffered attack at dash end; hit stun 0.3 s; speed, reach, hitbox) are also untouched.
- Movement is simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- The game loop uses variable delta; 30 and 60 FPS are supported.

Changes (described, not built or run; assumptions from the register are unverified against real code):
- Delta is capped at 0.05 s per update, including the first update after unpausing. State timers use delta, carry leftovers into the next state, and stop while paused.
- Room data holds waves (spawn list of type and slot), next-wave condition (K, T), Grub speed, Spitter interval and charge switch. Spawn timings (fade-in 0.8 s, first Spitter shot 1.0 s after fade-in, spawn wait at 4 tiles up to 2.0 s) are shared constants. Six slots: Door, Far, L, R, FL, FR, with coordinates in room data (actual values unknown).
- Room table (waves; K/T for wave 2; Grub speed; Spitter interval; charge switch):
  - R1: [Grub L, Grub R], [Grub Far]; K=1 T=10; 2.0; –; off.
  - R2: [Charger Far], [Grub L, Grub R, Charger Far]; K=0 T=15; 2.0; –; on.
  - R3: [Spitter Far, Grub L], [Spitter farther of FL/FR, Grub R]; K=1 T=12; 2.2; 2.0; off.
  - R4: [Spitter FL, Charger Far, Grub L], [Spitter FR, Charger R]; K=1 T=12; 2.2; 1.8; on.
  - R5: [Spitter Far, Grub L, Grub R], [Spitter farther of FL/FR, Charger L, Charger R]; K=1 T=12; 2.4; 1.6; on.
- Grub Chase speed per room (2.0, 2.0, 2.2, 2.2, 2.4) applies to both `grub` and `grub_charger` walking. It is not used for Charge (8.0).
- Spawner: wave 1 at room start. Wave N+1 spawns when living enemies ≤ K or T seconds after the last enemy of wave N finished fading in (after any wait), whichever is first. Living enemies include fading-in enemies and exclude those waiting at a slot. K and T are checked only once every enemy in wave N has started fading in; this start point is logged and set in one place. For waves without waiting enemies it is the spawn decision.
- Slot waiting: per slot, all slots of a wave start waiting together at the spawn decision; player-to-slot center distance under 4 tiles waits up to 2.0 s. A slot that finished waiting does not wait again. The player is not pushed out of a slot.
- Far corner choice (FL or FR): chosen at the spawn decision before waiting, by center-to-center distance from the player to each slot coordinate; farther wins, FL on exact ties; fixed during the wait. Does not apply to a corner named as a fixed slot for another enemy.
- Charge switch: one place in the spawner replaces `grub_charger` with `grub` when off. No visuals are added in that case.
- Spawning state for all enemies: 0.8 s, no movement, no action, no damage to the player, no damage or flinch from the player. Then Chase.
- Spitter projectile: 4.0 tiles/s, 1 heart, straight to the player's position at firing, vanishes on walls, passes through enemies. Flinch unchanged.
- `grub_charger`: Grub data (HP 2, room Grub speed) plus charge numbers, same controller, states Spawning, Chase, Windup 0.7 s, Charge, Recovery 0.8 s. Charge goes at 8.0 tiles/s in a direction fixed at Windup start, to 7.0 tiles or a wall; leftover distance converts to time carried into Recovery.
- Windup entry conditions: ≥1.5 s since Spawning ended; ≥2.5 s since the previous Recovery ended (the moment it returned to Chase, not the end of Charge; the 0.8 s Recovery is excluded; a charger that has never been through Recovery counts as satisfied; flinch does not reset); player distance 3.0–6.0 center to center; no other living `grub_charger` in Windup or Charge (derived by scanning enemies, no stored token). Earliest repeat: Charge end + 0.8 + 2.5 = +3.3 s. Update order for simultaneous eligibility is the existing enemy order.
- Contact resolution during Charge only, in one function: per-update swept overlap, first overlap per charge is the contact; already overlapping at charge start counts on the first Charge update. The invulnerability query reads the flag as seen this update. Invulnerable gives "slipped through" (no damage), otherwise the existing damage routine applies 1 heart once and the result is "hit". The result stays for the rest of the charge; it resets to unresolved at Windup and Charge start. The visuals read it.
- Damage routine change: Spawning enemies ignore hits. A `grub_charger` in Windup, Charge or Recovery loses HP only, with no Flinch, knockback or state/direction/timer change. All other cases flinch 0.2 s. HP 0 kills immediately in any state.
- Visuals (stage 0 art, no reduced fallback): fade-in with a blue ring; ember ridge overlay on charge-type Grubs only; floor lane drawn below characters and projectiles, self-lit, clipped to 7 tiles or the wall using the charge collision test, width from the enemy contact width value; body squash/stretch is render-only; afterimages every 0.5 tiles; one new particle type (afterimage, dust, steam, sparks); white hit flash 0.1 s; crack overlay at HP 1; pale ring at the player for 0.15 s on "slipped through". No audio.
- Dev build only: room select 1–5, per-room charge switch, 30/60 FPS toggle, and a state transition log (including the wave all-fading-in moment and, new in this build, each `grub_charger`'s Recovery end time). No new player inputs.

Open assumptions (unconfirmed): contact shape and size of enemies; slot coordinates; whether other enemy timers (bite interval) use delta; room end condition coupling to wave spawning; lane/projectile/lantern color similarity.
>>>END

<<<FILE sim/build-0.5.md
# Simulated build 0.5 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. Lengths are in seconds, distances in tiles, speeds in tiles per second. Everything below holds the same at 30 FPS and 60 FPS unless a difference is stated.

## Rooms and waves

- Every room sends its enemies in two waves. The first wave appears when the room starts. The second wave appears when the number of living enemies drops to the room's threshold, or when the room's timer runs out, whichever happens first.
- Enemies that are fading in count as living. Enemies still waiting to appear do not count.
- The timer starts when the last enemy of the earlier wave has finished fading in. If that enemy had to wait at its spot first, the timer starts after the wait and the fade-in.
- Room 1: wave 1 is two ordinary Grubs, left and right. Wave 2 is one ordinary Grub at the far side. It comes when one or fewer enemies are alive, or 10 s after the last wave-1 Grub finished fading in. 3 enemies in total, at most 2 at once. No charging Grubs.
- Room 2: wave 1 is one charging Grub at the far side. Wave 2 is two ordinary Grubs (left, right) and one more charging Grub (far side). It comes when no enemy is alive, or 15 s after the wave-1 Grub finished fading in. 4 enemies in total, at most 3 at once.
- Room 3: wave 1 is a Spitter at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in whichever far corner is farther from you at the moment the wave is triggered, and an ordinary Grub on the right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 4 enemies in total, at most 3 at once. Spitters fire every 2.0 s. No charging Grubs.
- Room 4: wave 1 is a Spitter in the far-left corner, a charging Grub at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in the far-right corner and a charging Grub on the right. It comes when one or fewer are alive, or 12 s. 5 enemies in total, at most 3 at once. Spitters fire every 1.8 s.
- Room 5: wave 1 is a Spitter at the far side and two ordinary Grubs, left and right. Wave 2 is a Spitter in the farther far corner and two charging Grubs, left and right. It comes when one or fewer are alive, or 12 s. 6 enemies in total, at most 4 at once. Spitters fire every 1.6 s.
- A room ends when every wave has appeared and every enemy is dead.
- The farther-corner choice is made when the wave is triggered, before any waiting. The two corners are compared by distance from the center of you to the center of each spot. If the distances are exactly equal, the front-left corner is used. If you move while the wave waits, the choice does not change. A corner that a room names for a specific enemy is not part of this choice.

### How fast Grubs walk

Ordinary and charging Grubs in the same room walk at the same speed:
- Room 1: 2.0
- Room 2: 2.0
- Room 3: 2.2
- Room 4: 2.2
- Room 5: 2.4

This is walking speed only. A charge always runs at 8.0. Spitters stand still.

### Standing near a spawn point

- If you are closer than 4 tiles (center to center) to the spot where an enemy would appear, that enemy does not appear yet. It appears as soon as you are 4 tiles or farther away, or after 2.0 s of waiting, whichever comes first.
- Each spot of a wave waits on its own. All spots of one wave start waiting at the same moment, when the wave is triggered. A spot that has finished waiting does not wait again if you walk back to it. You are not pushed away from a spot, and the enemy can appear on top of you.
- While some enemies of a wave are still waiting, the next wave's threshold and timer are not running. They start only once every enemy in the wave has begun fading in.
  - If one or fewer enemies are alive at that moment, the next wave comes immediately. Otherwise it comes when the count drops to the threshold, or when the timer runs out.
  - Room 1: stand near the left spot only. The right Grub appears and the second wave does not come while the left spot waits. If you kill the right Grub during the wait, then when the left Grub begins fading in only one enemy is alive, and the wave-2 Grub comes at once. If you did not kill it, the second wave comes after one is killed, or 10 s after the later one finished fading in.
  - Room 2: if the charging Grub's spot is waiting, the second wave cannot come until it begins fading in. After that it comes when the Grub is dead, or 15 s after it finished fading in. The Grub cannot be hurt during its first 0.8 s of fading in, so the earliest kill is after that.
  - Waves with no waiting spots start counting the moment they appear.

## Enemies appearing

- Every enemy fades in for 0.8 s: from 40% to full opacity, with a pale blue ring at its feet. During this time it does not move, does not attack, does not hurt you, and your swipes do nothing to it (no damage, no flinch).
- A Spitter fires its first shot 1.0 s after it finishes fading in, then at the room's interval. A Spitter shot travels at 4.0, straight at where you stood when it fired, costs 1 heart, vanishes on walls, and passes through enemies without hurting them. Spitters flinch for 0.2 s when hit, as before.

## Charging Grubs

Charging Grubs (rooms 2, 4, 5) look like ordinary Grubs with a dark ember-colored ridge on the back, visible from the moment they fade in. Ordinary Grubs have no ridge. They have 2 HP, and walk and bite like ordinary Grubs. While walking they flinch for 0.2 s when hit.

A charging Grub starts a charge only when all of the following hold:
- at least 1.5 s have passed since it finished fading in;
- at least 2.5 s have passed since its last recovery ended, that is, since it went back to walking after its last charge. The 0.8 s of recovery is not part of the 2.5 s. For example, if a charge ends at time t, the Grub stands in recovery until t+0.8, and its next wind-up can begin no earlier than t+3.3. A Grub that has never charged has no such wait;
- you are 3.0 to 6.0 tiles away (center to center);
- no other living charging Grub is currently winding up or charging.

Flinching does not reset these waits. If two charging Grubs qualify in the same moment (room 5, wave 2, left and right), one of them goes first, in a fixed but not obvious order. The other waits until the first has finished charging.

The sequence:
1. **Wind-up, 0.7 s.** The Grub stops where it stands and its walking animation stops. A red-orange lane appears on the floor from the Grub toward where you were when the wind-up began. The lane is as long as the charge will be, 7 tiles or less if a wall is in the way, and as wide as the Grub's body (within 0.1 tile). It has a bright edge, a dark underline and a chevron every tile pointing along the lane. It stays lit regardless of floor darkness. Spitter shots, fading-in enemies and other enemies are drawn on top of it. The lane fades from 35% to full brightness over the wind-up. The Grub squashes to 80% height, widens a little and leans back from the lane. The ridge and eyes warm from dark to red-orange, turning pale-yellow in the final 0.1 s. The direction is fixed; moving afterwards does not turn the lane. The Grub does no damage during the wind-up.
2. **Charge.** The Grub rushes along the lane at 8.0 for up to 7 tiles (about 0.875 s), or until it hits a wall, and stretches long and thin with a bright core and red-orange edge. The lane flashes extra bright once at the start, stays at full brightness, and disappears behind the Grub as it passes. The part in front stays until the charge ends, then everything fades out over 0.1 s. Afterimages appear every half tile and fade over 0.2 s, with dust at its feet. It passes through other enemies without hurting them. Hitting a wall has no special effect; the Grub simply stops and goes into recovery.
3. **Recovery, 0.8 s.** The Grub stands still, sunk to 90% height and tinted a dull grey-blue, fully opaque, with thin steam rising from its feet every 0.3 s. Ridge and eyes go dark within 0.1 s. It returns to normal in the last 0.2 s and goes back to walking toward you. It cannot start another wind-up for 2.5 s after this moment.

### Getting hit by a charge

- A charge can hurt you at most once. The first time the Grub's body overlaps you during a charge decides it. If it was already overlapping you as the charge began, that counts as the first moment.
  - If you are invulnerable at that moment (for example, mid-dash), you take nothing. A thin pale white-blue ring appears around you for 0.15 s, and the Grub keeps running through you. The Grub's core dims to a darker red-orange for the rest of the charge. Staying inside it afterward, or the dash ending while it still overlaps you, does not hurt you.
  - If you are not invulnerable, you lose 1 heart, with the normal hit reaction and the normal invulnerability afterward. The core dims in the same way. No ring appears.
- Overlap during the wind-up or recovery does nothing. A new charge starts the count again.
- The invulnerability check uses the state you are in at that frame. At 30 FPS the end of the dash's 0.25 s protection can differ from 60 FPS by up to one frame (about 0.034 s).

### Hitting a charging Grub

- During the wind-up, charge and recovery, your swipes lower its HP only. It does not flinch, is not pushed back, and does not change direction, speed or timing. It flashes white for 0.1 s with small sparks at the point of impact. The lane and ridge do not change.
- With 1 HP left, a small crack mark appears on its body.
- At 0 HP it dies immediately in any state. A dying winder or charger removes its lane within 0.1 s, and another charging Grub may then start its own wind-up.
- Charging Grubs that are walking, ordinary Grubs and Spitters flinch 0.2 s as before.

## Your own numbers

Nothing about you has changed:
- Your swipe does 1 damage and takes 0.35 s to recover.
- Your dash covers 4 tiles in 0.25 s, you are invulnerable for all of it, and it has a 0.6 s cooldown. A swipe pressed during a dash comes out when the dash ends.
- A hit costs 1 heart, locks your input for 0.3 s, and you are invulnerable until 0.8 s after the hit.
- Movement speed, swipe reach and your size are unchanged. No new buttons.

## Timing at 30 and 60 FPS

- Fade-in, wind-up, charge distance, recovery, the 2.5 s wait, wave timers and spawn waiting are all counted in real time. Durations at 30 FPS are within about 0.034 s of those at 60 FPS.
- Whether a charge touches you does not depend on the frame rate.
- Pausing freezes all timers and animations, including lanes, steam and rings. Resuming after a long pause does not skip ahead more than a short step (0.05 s).
- Nothing flashes more than three times per second, apart from single flashes.

## What play feels like now

- Rooms 1 and 3 behave like before but with two waves, so there is a second arrival to deal with.
- In rooms 2, 4 and 5, standing still in a corner and swiping no longer works: a lane appears, and about 0.7 s later a Grub runs the length of it. Moving off the lane or dashing through the Grub avoids damage. Swiping the Grub during the run only chips it and does not stop it.
- A single charging Grub charges again about 3.3 s or more after its previous charge ended, and later if you are out of the 3.0–6.0 range or another one is busy.
- Only one charging Grub is ever winding up or charging at a time.
- No new sounds. No new buttons.
- As before, occasionally, if you dash right after being hit, you take damage partway through the dash. This also applies to a charge that reaches you at that moment.

## Development build only

- A tester can pick room 1–5, switch charging Grubs on or off per room (off turns every charging Grub into an ordinary Grub, with no ridge, no lane and no charge; the room's counts, waves and spots stay the same), and switch between 30 and 60 FPS.
- A log lists state changes with game time, enemy and type, charge direction, contact result (unresolved, slipped through, hit), wave arrivals with spots, which corner was chosen, the distance to you when a wind-up began, and the moment all enemies of a wave have begun fading in.
- The log also records the time each charging Grub's recovery ended and it went back to walking, so the gap to its next wind-up can be read directly.
>>>END

<<<FILE decisions/D-005-flinch-contact-and-far-slot-rules.md
---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-005: 突進型は 3 状態で怯まない、接触は突進ごとに最初の重なりで 1 回だけ解決する、「遠い方」は出現を決める時点で選ぶ

## Decision

技術確認(Handoff 08)で見つかった仕様と既存実装の食い違い 3 点を、D-002、D-003 の範囲内で次のとおり決める。`design/combat.md` に反映済み。数値は変えていない。

1. **怯み(Flinch)**: 突進型 Grub の Windup、Charge、Recovery の間は怯まない(ダメージは受ける。HP 0 で倒れる)。ノックバックが既存にあっても、この 3 状態の間は受けない。Chase など他の状態、通常型 Grub、Spitter の怯み(0.2 s)は既存のまま。出現中はダメージ自体を受けない(既存の仕様どおり)。Chase 中の怯みで突進の開始条件のタイマーは巻き戻さない。
2. **接触の定義(案 A)**: Charge 中の接触は、1 回の突進につき、体が最初に重なった瞬間(更新ごとのスイープ判定。Charge 開始時にすでに重なっていれば開始の瞬間)に 1 回だけ解決する。その時点で無敵ならダメージなしで、その突進はその後もうダメージを与えない。無敵でなければ 1 ハートを 1 回だけ与え、その後は与えない。ダッシュの窓は、接触の瞬間の 0.25 s 前から接触の瞬間まで(幅 0.25 s のまま)。Chase 中の噛みつきは対象外(既存のまま)。
3. **「FL または FR のうち遠い方」**: 部屋 3 と部屋 5 の波 2 で同じ規則。その波の出現を決める時点(出現位置の待ちの前)のプレイヤー位置から各スロット座標までの距離を比べ、遠い方を選ぶ。同距離は FL。待ちの間は選び直さない。

あわせて、技術側の既定(Handoff 09 の既定 4)を承認する: 「T s」の起点はその波の最後の敵の出現中の終わり、「生きている敵」は出現中の敵を含む、出現位置にプレイヤーが重なっても押し出さない。

**この決定が扱わないこと**: 欠陥 D(被弾直後のダッシュ中のダメージ)の規則。プレイヤー側の数値。ダッシュの窓の変更(0.25 s のまま)。

## Rationale

- 怯み: 怯むと Windup、Charge が途中で止まり、予告が「害を与える前の合図」にならない。Charge が攻撃一発で止まれば、ダッシュで抜ける場面の前提(止められない突進)も崩れる。D-003 の規則(方向固定、予告中は無害、同時 1 体)と整合するのは、3 状態で怯まない解釈。Recovery を怯まないままにするのは、反撃の隙の長さ(0.8 s)を一定に読ませ、2 回振れる(§3.6)ことを保つため。通常の状態の怯みは既存のままなので、既存の手触りは変わらない。
- 接触: 案 B(重なっている間ずっと判定)では、窓が重なりの長さ(約 0.1〜0.2 s)ぶん狭くなり、0.25 s の無敵のうち実際に使える部分が小さくなる。「ダッシュで抜けられる」(D-002 の位置づけ、C の検証)が成り立ちにくい。案 A は、仕様の意図(接触を 1 点の瞬間として数える)と、V3 の測定の定義をそのまま保つ。ダッシュが重なりの途中で終わっても被弾しない点は、「抜けた」という結果を素直に見せる。窓の数値は変えないので、プレイヤー側の数値を H1 前に触らない方針とも合う。
- 遠い方: 部屋 3 と同じ規則にすれば、読む規則が 1 つで済み、データだけの変更で直せる。出現を決める時点で固定すれば、待ちの間のプレイヤーの動きで結果が揺れず、検証が再現できる。
- 既定 4: 「最後の敵の出現中の終わり」を起点にすると波が早く出すぎない。出現中の敵を数えると、K の判定が出現の瞬間にずれない。押し出さないのは、出現中が無害で見えるため。

## Alternatives considered

- **怯みを全状態で無効にする / 全状態で既存のままにする**: 前者は通常の Chase の手触りまで変わる。後者は予告と突進が攻撃で壊れる。どちらも採らない。
- **Recovery だけ怯みを残す**: 反撃で Recovery が中断され、Chase への復帰が早まり、隙の長さが一定でなくなる。採らない。
- **接触を重なっている間ずっと判定する(案 B)**: 窓が狭くなる。窓を補うには無敵時間などプレイヤー側の数値を触る必要があり、D-002 の範囲外。採らない。
- **接触の窓を 0.25 s より広げる**: プレイヤー側の数値の変更にあたり、H1 の確認前は行わない。
- **「遠い方」を待ちのあとに選び直す**: 動いたプレイヤーに合わせて位置が変わり、検証と読みが不安定になる。採らない。

## Revisit when

- Play で、ダッシュの窓(0.25 s)が「使える」と感じられない、またはダッシュで抜けたのに当たったと感じられる場合。
- 突進型が攻撃で全く止まらないことが、「理不尽」と感じられる場合(Recovery の怯み、または Charge 中の被ダメージの見せ方を再検討)。
- 欠陥 D の再現で、無敵の規則が変わり、接触の瞬間の読み取りの前提が変わる場合。
- 技術側で、最初の重なりの検出(スイープ判定)が既存の判定形状で扱いにくいとわかった場合。
>>>END

<<<FILE decisions/D-009-wave-condition-start-and-waiting-enemies.md
---
kind: decision
id: D-009
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-009: 次の波の K と T は、前の波の全員が出現中に入った時点から調べ始め、出現位置の待ちの敵は「生きている敵」に数えない

## Decision

`design/combat.md` §4.1 の欠落を、D-002、D-003、D-005 の範囲内で次のとおり決める(案 A)。

- 波 N の次の波の K と T は、**波 N の全員が出現中に入った時点**から調べ始める。それより前は、K の判定も T の計測もしない。
- 出現位置の待ち(プレイヤーがスロットから 4 タイル未満、最大 2.0 s)に入っている敵は、「生きている敵」に**数えない**。出現中に入った時点から数える(D-005 の「出現中の敵を含む」はそのまま)。
- T の起点は、D-005 で承認した定義のまま(その波の最後の敵の出現中が終わった時点)。
- 全員が出現中に入った時点で生きている敵が K 体以下なら、すぐ次の波を出す。そうでなければ、K 体以下になるか T s たつかの先に起きた方。
- 待ちがない波では、出現を決めた時点が調べ始める時点になる(従来どおり、挙動は変わらない)。
- 待ちはスロットごとに別々で、同じ波の待ちは同時に始まる。待ちの間にプレイヤーが 4 タイル以上離れたら、そのスロットの待ちはその時点で終わる。いったん終わったスロットは待ち直さない。追加の規則は不要(既存の文面の明記)。

数値(K、T、0.8 s、4 タイル、2.0 s、部屋の構成)は変えていない。受け入れ基準は V7 を更新し、V12 を足した。

**この決定が扱わないこと**: 欠陥 D。プレイヤー側の数値。波の数や部屋の構成の変更。

## Rationale

- 文面どおりに読むと、部屋 2(K=0)は、プレイヤーが出現位置の近くに立つだけで波 1 の敵が「いない」ことになり、波 2 が即座に出る。部屋 1(K=1)でも片方が待つだけで同じことが起きる。プレイヤーの立ち位置で波が早まり、構成の進行(D-002 の主軸)が崩れる。
- 案 A は、「すべての波が出現し」という既存の文、T の起点の定義(最後の敵の出現中の終わり)と矛盾しない。調べ始める時点が T の起点より前に必ず来るので、順序が一貫する。
- プレイヤーに見える挙動で検証できる。「敵が現れていない間は次の波が出ない」と確認できる(V12)。
- 費用はスポナーの 1 か所の判定で小さい。実装側の提案とも一致する。

## Alternatives considered

- **案 B(待ちの敵を「生きている敵」に数える。調べ始めるのは前の波の出現が決まった時点)**: 数え方は単純だが、まだ現れていない敵で K を満たす。部屋 2 では、突進型を倒す(K=0)前に T の計測が始まり、待ちが長いほど T が実質的に短くなる。プレイヤーの立ち位置で波 2 の時機がずれる。見た目と数がずれ、検証もしにくい。採らない。
- **案 C(別の規則)**: 待ちの間だけ K を凍結するなどの規則は、案 A より複雑で、得るものがない。採らない。

## Revisit when

- Play で、出現位置の近くに立つと波 2 が遅く感じられる、あるいは待ちを使って波を引き延ばせると分かった場合(待ちの上限 2.0 s や 4 タイルの調整を検討)。
- 波が 3 以上の部屋を作る場合(同じ規則を波 N → N+1 に適用するが、確認する)。
- 技術側で、全員が出現中に入った時点の判定が既存のスポナーで扱いにくいとわかった場合。
>>>END

<<<FILE goals/G-001-combat-monotony/34-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 34
from: qa
to: studio
stage: Verify
outcome: question
---
# 34: qa → studio — 模擬ビルド 0.5 の再検証結果(F-1、V10、V12(c) は解消。V7 の同距離の規則だけ、記述の用語が仕様と合うか確認不能)

## Task

`sim/build-0.5.md` を `design/combat.md` の V1〜V12 に照らして再検証した結果を報告する。Studio は、V7 の「同距離のとき FL」の確認不能 1 点をどこに回すか決めてほしい。

## Context

G-001、Verify。**この報告はすべて「模擬ビルドの記述に基づく」(D-008)。実機で観測した証拠ではない。** 判定は、仕様(`design/combat.md`、D-005、D-009)とビルド記述だけから行った。実装側の説明や自己評価は使っていない。前回は Handoff 30(ビルド 0.4)。

## Findings

### 総合判定

- fail の基準はない。重点の 4 点のうち、F-1、V10、V12(c) は解消した。V7 のうち、Grub 速度の数値と「中心間の距離」「出現を決める時点で選ぶ」「選び直さない」は確認できた。
- **V7 の「同距離のときは FL」だけは pass にできない**(下記)。そのため outcome は `pass` ではなく `question`。
- 同じ基準が 2 回目の fail になった例はない。F-1 は前回と同じ点だが、今回は食い違わない。戻りルール(`technical-director`)は発動しない。

### 重点 4 点

**1. F-1(§3.3 再突進の待ち時間の起点): 解消(pass、模擬)**
- ビルドの開始条件に「最後の recovery が終わってから 2.5 s 以上。recovery の 0.8 s は 2.5 s に含まれない」とある。
- 例も書かれている。突進が時刻 t に終わると、recovery は t+0.8 まで続き、次の wind-up は早くても t+3.3。これは仕様の期待値(t + 0.8 + 2.5 s)と一致する。
- 「Recovery の項」にも、「この時点(recovery の終わり)から 2.5 s は次の wind-up に入れない」とある。「遊んだときの感触」の項にも、前回の突進が終わってから約 3.3 s 以上とある。3 か所の記述は互いに矛盾しない。
- 一度も突進していない Grub には、この待ちがない。仕様でも、待ちの対象は「前回の Recovery」なので、整合する。
- 怯みで待ちを巻き戻さない記述も、仕様の §2.1 と一致する。
- 時間は実時間で数える(30/60 FPS の差は約 0.034 s 以内)。開発用ログに、各 Grub の recovery の終了時刻が残る。次の wind-up までの間隔を直接読めるので、実機で確かめやすい。
- 前回(Handoff 30)の食い違いは、記述上は解消している。

**2. V7: 一部確認不能(question)**
- Grub 速度: 部屋 1〜5 が 2.0 / 2.0 / 2.2 / 2.2 / 2.4。仕様と一致。通常型と突進型は同じ速度。突進は 8.0 のまま。**pass**。
- 部屋の構成、K と T、Spitter 間隔、合計数と同時最大数(3/2、4/3、4/3、5/3、6/4)は、仕様の §4.3 と一致。前回と同じ。**pass**。
- 「遠い方」:
  - 比べる距離は、プレイヤーの中心から各スロットの中心まで。波を出す時点で、待つ前に選ぶ。待ちの間に動いても選び直さない。部屋が別の敵に指定している角は、この選択の対象外。いずれも仕様と一致。**pass**。
  - **同距離のとき**: ビルドは「完全に同じ距離なら front-left corner を使う」と書いている。仕様の FL は「奥の左隅」(far-left)。ビルドは部屋 4 の記述では同じスロットを「far-left corner」と呼んでいて、同距離の規則だけが「front-left」になっている。
  - 「front-left」が FL(奥の左隅)の略なのか、別の角を指すのか、ビルドの記述からは決められない。字面どおりに読むと、選択の対象ではない手前の角になる。推測で pass にはしない。**確認不能**。
  - 規則そのものは仕様で定義されていて、期待値は未定義ではない。Design に回す問題ではない。ビルドの記述の用語の確認が要る。
  - 確認の方法の候補: (i) 記述を「奥の左隅(FL)」に直してもらう。(ii) 開発用ビルドで、2 つの角から完全に等距離の位置に立って波を出し、ログの「選ばれた角」が FL になることを見る。

**3. V10: pass(模擬)**
- 「Your own numbers」の項に、次の数値が書かれている。
  - 攻撃: 1 ダメージ、回復 0.35 s。
  - ダッシュ: 0.25 s で 4 タイル、ずっと無敵、クールダウン 0.6 s、ダッシュ中に押した攻撃は終了時に出る。
  - 被弾: 1 ハート、硬直 0.3 s、被弾から 0.8 s 後まで無敵。
  - 移動速度、攻撃の届く距離、プレイヤーの大きさは変更なし。新しいボタンもない。
- どれも §1 と一致する。前回は記述がなくて確認できなかった項目が、今回は数値つきで書かれている。

**4. V12(c): pass(模擬)**
- 「Each spot of a wave waits on its own. All spots of one wave start waiting at the same moment, when the wave is triggered.」とある。同時に始まり、スロットごとに別々に数える。前回の指摘(同時に始まるという明記がない)は解消した。
- 待ちの間に 4 タイル以上離れると、その時点で出現中に入る(2.0 s を待たない)。いったん終わった待ちは、戻っても再開しない。
- 次の波の K と T は、波の全員が出現中に入るまで動かない。入った時点で生きている敵が 1 体以下なら、次の波はすぐ出る。部屋 1 の例で、待ちの間に右の Grub を倒すと、左が出現中に入った時点で波 2 が出ると書かれている。仕様の期待値と一致する。
- 待ちの時間は実時間で数える(30/60 FPS で差は約 0.034 s 以内)。
- 注意: 記述の例は左だけが待つ場合。右だけが待つ場合は、記述上は対称。同じ波の複数スロットが同時に待つ組み合わせは、部屋 1 と部屋 5 の波 2 などで作れる。実機のログで確認する価値がある。

### V1〜V12 の回帰結果

| 基準 | 結果 | 根拠(ビルド記述) |
|---|---|---|
| V1 | pass(模擬) | Wind-up 0.7 s → Charge → Recovery の固定順。開始条件に出現中の終了から 1.5 s 以上がある。ポーズは全タイマーを止め、復帰で 0.05 s までしか進まない。30/60 FPS の差は約 0.034 s 以内。 |
| V2 | pass(模擬) | 8.0 タイル/s、最大 7 タイル(約 0.875 s)または壁まで。方向は固定され、レーンは回らない。 |
| V3 | pass(模擬)。窓の端の数値は未測定 | 最初に重なった瞬間の無敵状態で決まる。ダッシュが重なりの途中で切れても被弾しない。30 FPS の端のずれは最大 1 フレーム。「窓から 0.05 s 外れると被弾」は規則から導けるが、数値の記述はなく、ログにダッシュ開始時刻もない。実機で測る必要がある。直前 0.8 s 以内の被弾は対象外(欠陥 D)。 |
| V4 | pass(模擬) | 1 回の突進で最大 1 回。最初の重なりが決める。開始時に重なっていれば開始の瞬間。無敵なら通り抜け、その後はダメージなし。Wind-up と Recovery の重なりは無害。次の突進で数え直す。 |
| V5 | pass(模擬) | 他の生きている突進型が Wind-up または Charge 中でないことが条件。倒れたらレーンが 0.1 s 以内に消え、別の Grub が始められる。 |
| V6 | pass(模擬) | スイッチをオフにすると、全突進型が通常型になる。数、波、出現位置は同じ。 |
| V7 | 一部確認不能 | 上記。 |
| V8 | pass(模擬) | 0.8 s のフェードイン。行動せず、ダメージを与えず、攻撃も効かない。押し出されない。 |
| V9 | pass(模擬) | 出現中の終了から 1.0 s で最初の弾。4.0、撃った瞬間の位置へ直進、1 ハート、壁で消える、敵を通り抜けて敵に当たらない。 |
| V10 | pass(模擬) | 上記。 |
| V11 | pass(模擬) | 突進型は 3 状態で怯まず、HP だけ減る。押し戻されず、方向、速度、タイミングも変わらない。HP 0 ならどの状態でも即死。Chase 中は 0.2 s 怯む。出現中は効かない。 |
| V12 | (a)(b)(c)(d) すべて pass(模擬) | (a) 部屋 2 は、待ちの間は波 2 が出ない。出現中に入ってからは、倒れる(K=0)か、出現中の終了から 15 s の早い方。(b) 部屋 1 は上記のとおり。(c) 上記。(d) 待ちのない波は出現した時点から数える。 |

その他の確認:
- 新しい入力ボタンなし、新しい音なし(D-001 に抵触しない)。点滅は 1 秒に 3 回を超えない。
- 30/60 FPS は、ビルドが「同じ」と述べている点を読んだだけ。別々の観測はしていない。
- 前回の V12 の補足(同時に始まる)は、今回は明記されている。

### 観察(基準外。V1〜V12 の fail にしない。原因は推測しない)

- **欠陥 D**: ビルドは今回も、「被弾の直後にダッシュすると、ダッシュの途中でダメージを受けることがある。そのときに届く突進にも当てはまる」と書いている。欠陥 D は検証の範囲外なので、fail にはしない。ダッシュで抜けたつもりが当たる場面が起こり得るので、Play の「抜けた」と感じられるか(§6.2)に影響しうる。期待される挙動は仕様で意図的に未定義。
- **用語**: 上記のとおり、同距離の規則だけ「front-left」と書かれている。他の箇所は far-left / far-right の表記。

## Decisions already made

- D-005: 怯み、接触、遠い方の規則(同距離は FL)。V7、V3、V4、V11 の判定の基準にした。
- D-008: 判定は模擬ビルドに基づく。結果に模擬であることを明記した。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。V7、V12 の判定の基準にした。

## Constraints

- この報告は模擬ビルドの記述に基づく。実機の証拠として扱わない。
- 見た目の A 系の基準は `art-director` の担当で、この報告の範囲外。
- QA は仕様の期待値を決めない。

## Open questions

1. **V7 の同距離の規則**: ビルドの「front-left corner」が仕様の FL(奥の左隅)を指すことを、どう確認するか。ビルド記述の修正(`gameplay-engineer`)か、等距離の位置でのログ確認。期待値は仕様で定義済みなので、`game-designer` の判断は要らない。
2. **欠陥 D**: Play の前に規則を決めるか、既知の欠陥として Play に渡すか。Handoff 30 から引き続き、Studio の判断。

## Expected output

Studio が上の 1 点の扱いを決める。解消したら、QA が V7 の同距離の規則だけを再確認し、他の基準が変わっていないことを確かめて pass にする。F-1、V10、V12(c) は再確認不要。pass になったら、Studio が Play (`playtester`)の Handoff を、実装の履歴を含まない形で組み直す。

## Load

- Role: none (Studio が読む)
- Skills: none
- Project: design/combat.md、sim/build-0.5.md
- Decisions: decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/33-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/32-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 32
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 32: gameplay-engineer → studio — 変更内容 2.1〜2.4 の修正版(F-1 の起点の明記、Grub 速度の数値、同距離の規則、プレイヤー側の数値)

## Task

Handoff 31 の指示により、変更内容(2.1〜2.4)を修正して全体を書く。Handoff 28 を読まなくても分かる形にする。F-1、V7 の未確認 2 点、V10 の未確認、V12(c) の補足を扱う。

## Context

G-001(戦闘の単調さ)。D-008 により、Build は変更内容を正確に書いた時点で完了する。実コードの変更、ビルド、テスト、動作確認は行っていない。以後の Verify 以降は、この記述からシミュレーターが作る模擬ビルドに基づく。実機の証拠ではない。

Handoff 30 では、V1〜V12 のうち fail はなかった。V7 と V10 の一部が記述から確認できず、仕様との食い違い F-1 が 1 件あった。

## Findings

### 0. 確認結果(Handoff 31 の Open questions への答え)

1. **F-1**: 仕様 §3.3 の文面は曖昧ではない。「前回の Recovery が終わってから 2.5 s 以上」で、仕様に合わせて直す。**Handoff 28 の 2.2 の条件 1 は、すでに「前回の Recovery が終わってから」と書いていた。** 模擬ビルド 0.4 が「突進が終わってから」と書いた理由は、変更内容の記述からは分からない。以下の修正版では、起点を Recovery の終了(Chase に戻った時点)と明記する。「Charge の終了ではない」と書き、数値の例も添える。確認のため、遷移ログに Recovery の終了時刻を足す(2.4)。
2. **遠い角が同距離のとき**: 仕様 §4.1 と D-005 に定義がある。距離は中心間で比べ、同じ距離なら FL を選ぶ。Handoff 28 は「同じ距離なら FL」と書いていたが、「中心間」と座標の取り方がなかった。修正版に明記する。
3. **Grub の速度**: 仕様 §4.3 の数値は 2.0 / 2.0 / 2.2 / 2.2 / 2.4(部屋 1〜5)。Handoff 28 の部屋表にはこの数値がすでにあった。模擬ビルドが数値を落とした理由は分からない。修正版では、部屋ごとの速度を表の外にも列挙し、どの敵に適用するかを書く。
4. **V10**: 変更しない数値を、修正版に列挙する(2.2 の末尾)。
5. **V12(c) の補足**: 同じ波の複数スロットの待ちが、波を出すと決めた時点から同時に始まる、という 1 文を足す。仕様 §4.1 と D-009 に矛盾しない。

### A. 修正後の変更内容(2.1〜2.4 の全体)

共通ルール: 長さは秒、距離はタイル、速度はタイル/秒。状態のタイマーはゲーム内の経過時間(delta)で進める。delta は 1 更新あたり 0.05 s を上限にする(ポーズ復帰の最初の更新も同じ)。状態が切り替わるときは余りを次の状態に持ち越す。ポーズ中は全部のタイマーと見た目の変化が止まる。数値は仕様の暫定値(P)のまま、変えていない。

#### 2.1 部屋とスポナー

**部屋データ**: 部屋ごとに、波(スポーン一覧 = 敵の種類とスロット)、次の波の条件(K、T)、Grub 速度、Spitter の撃つ間隔、突進スイッチを持つ。出現中(0.8 s)、Spitter の最初の 1 発(出現中の終了から 1.0 s)、出現位置の待ち(プレイヤーがスロットから 4 タイル未満なら最大 2.0 s)は全部屋共通の定数にする。スロットは Door、Far、L、R、FL、FR の 6 つで、座標は部屋データで与える。

**部屋の構成**(「突進型」= `grub_charger`):

| 部屋 | 波 | 構成(スロット) | 次の波の条件 | Grub 速度 | Spitter 間隔 | 突進スイッチ |
|---|---|---|---|---|---|---|
| 1 | 1 | 通常 Grub × 2(L, R) | | 2.0 | – | オフ |
| | 2 | 通常 Grub × 1(Far) | K=1, T=10 s | | | |
| 2 | 1 | 突進型 Grub × 1(Far) | | 2.0 | – | オン |
| | 2 | 通常 Grub × 2(L, R) + 突進型 Grub × 1(Far) | K=0, T=15 s | | | |
| 3 | 1 | Spitter × 1(Far)+ 通常 Grub × 1(L) | | 2.2 | 2.0 s | オフ |
| | 2 | Spitter × 1(FL / FR のうち遠い方)+ 通常 Grub × 1(R) | K=1, T=12 s | | | |
| 4 | 1 | Spitter × 1(FL)+ 突進型 × 1(Far)+ 通常 Grub × 1(L) | | 2.2 | 1.8 s | オン |
| | 2 | Spitter × 1(FR)+ 突進型 × 1(R) | K=1, T=12 s | | | |
| 5 | 1 | Spitter × 1(Far)+ 通常 Grub × 2(L, R) | | 2.4 | 1.6 s | オン |
| | 2 | Spitter × 1(FL / FR のうち遠い方)+ 突進型 × 2(L, R) | K=1, T=12 s | | | |

表の読み方: 波 2 の行の K と T は、その波 2 を出す条件である。波 1 の全員が出現中に入った時点から調べる(下の「波の条件を調べ始める時点」)。

**Grub 速度の数値(Chase で歩く速さ)**:
- 部屋 1: 2.0 タイル/s。
- 部屋 2: 2.0 タイル/s。
- 部屋 3: 2.2 タイル/s。
- 部屋 4: 2.2 タイル/s。
- 部屋 5: 2.4 タイル/s。
- その部屋の通常型 Grub と突進型 Grub の Chase(歩き)に、同じ値を使う。突進の速度 8.0 タイル/s とは別の値で、Charge には使わない。Spitter は動かない。

合計は 部屋 1: 3 体、2: 4 体、3: 4 体、4: 5 体、5: 6 体。同時に存在する敵の最大は 部屋 1: 2、2: 3、3: 3、4: 3、5: 4。部屋は、全部の波が出現し、全部の敵が倒れたときに終わる(既存の終了条件はそのまま使う)。

**スポナーの動き**:
- 波 1 は部屋の開始時に出す(各スロットの出現位置の待ちは次項)。
- 波 2 以降は、「生きている敵が K 体以下」または「前の波の最後の敵の出現中が終わってから T s」の先に起きた方で出す。「生きている敵」には出現中の敵を含める。T の起点は、その波の最後の敵の出現中が終わった時点(出現位置の待ちがあれば、待ちが終わって出現中も終わった時点)である。
- **波の条件を調べ始める時点(D-009)**: 波 N の次の波(N+1)の K と T は、波 N の全員が出現中に入った時点から調べ始める。それより前は、K の判定も T の計測もしない。そのため、出現位置の待ちに入っている敵は「生きている敵」に数えず、出現中に入った時点から数える。
  - 全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波を出す。そうでなければ、K 体以下になるか T s たつかの先に起きた方で出す。T の起点は上のとおりで変わらない。
  - 待ちの敵がいない波では、出現を決めた時点が、そのまま調べ始める時点になる(従来どおり)。
- **出現位置の待ち**: スロットごとに、出現の時点でプレイヤーとスロット座標の距離(中心間)が 4 タイル未満なら待つ。距離が 4 タイル以上になるか、待ちが 2.0 s に達したら、そのスロットの敵が出現中に入る。待ちはスロットごとに別々に数える。**同じ波の複数のスロットの待ちは、波の出現を決めた時点から同時に始まる。**(仕様 §4.1、D-009。追加の規則ではない。)いったん待ちが終わったスロットは、プレイヤーが戻ってきても待ち直さない(仕様 §4.1 の既存の文面)。プレイヤーがスロットに重なっていても押し出さない。
- **「FL / FR のうち遠い方」(部屋 3 の波 2、部屋 5 の波 2)**: その波の出現を決める時点(出現位置の待ちを始める前)のプレイヤーの位置から、FL のスロット座標と FR のスロット座標までの距離を、**それぞれ中心間の距離**で比べ、遠い方を選ぶ。**2 つの距離が等しいときは FL を選ぶ**(仕様 §4.1、D-005)。選んだあと、待ちの間にプレイヤーが動いても選び直さない。同じ波で FL か FR が別の敵のスロットとして指定されている場合は、この規則の対象外(固定のスロットが優先)。
- **突進スイッチ**: スポナーが敵を生成する 1 か所で、スイッチがオフなら `grub_charger` を `grub`(通常型)に置き換える。敵の数、波、スロット、K/T は変わらない。スイッチがオフでも、尾根の重ね絵など突進の見た目は何も付かない。部屋 1、3 には突進型がいないので、スイッチは効かない。

#### 2.2 敵コントローラ(共通)

**出現中(Spawning)**: 全種類の敵に追加する。長さ 0.8 s。この間は、動かない、行動しない、ダメージを与えない、プレイヤーの攻撃のダメージも怯みも受けない。終わると通常の状態(Chase)に入る。Spitter の最初の 1 発は出現中の終了から 1.0 s 後。以降は部屋ごとの間隔。

**Spitter の弾**: 速度 4.0 タイル/s、ダメージ 1 ハート。撃った瞬間のプレイヤーの位置へ直進(先読みなし)。壁で消え、敵の体を通り抜けて敵にダメージを与えない。弾の仕組みは作り直さない。Spitter 自身の怯みは既存のまま(0.2 s)。

**`grub_charger`(突進型)**: Grub のデータ(HP 2、Chase の速度は部屋の Grub 速度)に突進の数値を足したもの。別のコントローラは作らない。状態は Spawning、Chase(既存)、Windup、Charge、Recovery。通常型 Grub と同じ Chase、噛みつき、怯みの既存のルーチンを使う。

| 状態 | 長さ | 動き | 接触ダメージ | 怯み・ノックバック |
|---|---|---|---|---|
| Chase | 条件まで | 部屋の Grub 速度で歩く(既存の移動) | あり(既存の噛みつき、1 ハート) | 既存(0.2 s) |
| Windup | 0.7 s | その場で停止、歩行アニメーションも止める | なし | なし |
| Charge | 7.0 タイル進むか壁まで | 固定した方向へ 8.0 タイル/s で直進 | 突進ごとに 1 回まで(下記) | なし |
| Recovery | 0.8 s | その場で停止 | なし | なし |

**Chase → Windup の条件**(Chase の各更新で調べる。すべて満たすとき):
1. 次の 2 つの待ち時間が両方たっている。
   - (a) 出現中が終わってから 1.5 s 以上。
   - (b) **前回の Recovery が終わってから 2.5 s 以上。** 起点は、前回の Recovery が終わって Chase に戻った時点である。**前回の Charge が終わった時点ではない。**Recovery の 0.8 s は 2.5 s に含めない。例: Charge が時刻 t で終わると、Recovery は t から t+0.8 まで。次の Windup が始まれるのは、早くても t+0.8+2.5 = t+3.3 以降。まだ Recovery を一度も経ていない Grub は、(b) を満たしているとみなす。
2. プレイヤーとの距離(中心間)が 3.0〜6.0 タイル。
3. この Grub が `grub_charger` である(スイッチがオフなら生成されない)。
4. 生きている他の `grub_charger` が Windup または Charge にいない。Windup に入る瞬間に、生きている敵を調べて導く。保存する状態(トークン)は作らない。

Chase 中の怯みでこれらの待ち時間は巻き戻さない(起点は出現中の終了と前回の Recovery の終了で、怯みは影響しない)。

**Windup**: 入る瞬間のプレイヤーの中心へ向かう単位ベクトルを突進方向として固定する(距離が 3.0 タイル以上なので零ベクトルにならない)。その後プレイヤーが動いても変えない。0.7 s たつと Charge に入る(余りは持ち越す)。

**Charge**: 毎更新 8.0 × delta の距離を固定方向へ進む。通算 7.0 タイルに達するか、既存の移動処理が壁で止めたら終わり、すぐ Recovery に入る(壁に当たったときの特別な処理はない)。7.0 タイルを超えた分は、時間に直して(超過距離 ÷ 8.0)Recovery の経過時間に持ち越す。他の敵の体は通り抜け、ダメージを与えない。

**Recovery**: 0.8 s たつと Chase に戻る。この戻った時点が、上の条件 1(b) の起点になる。

**接触の解決(1 つの関数)**:
- Charge 中の接触だけを扱う。Chase 中の噛みつきは含めない(既存のまま)。
- 毎更新、Grub とプレイヤーの相対運動をスイープで調べ、突進ごとに最初に体が重なった更新を接触の瞬間とする。Charge に入った時点ですでに重なっていれば、Charge の最初の更新を接触の瞬間とする。Windup と Recovery の間の重なりは数えない。
- 接触の瞬間に、プレイヤーの無敵を問い合わせ関数で読む(1 つの真偽。署名は変えない。その更新で見えているフラグの値を使う)。
  - 無敵なら: ダメージなし。結果を「抜けた」にする。Grub は通り抜けて走り続ける。
  - 無敵でなければ: 既存のダメージ処理で 1 ハートを 1 回だけ与える。結果を「被弾」にする。被弾後の硬直と無敵は既存の処理に任せる。
- 結果が決まったあと、その突進は、重なりが続いても、無敵が切れても、もうダメージを与えない。次の突進では、また最初の重なりから数える。
- 無敵のタイマーのコードには触れない。問い合わせ関数もフラグを読むだけで、意味づけは足さない。
- 接触結果(未解決 / 抜けた / 被弾)を Grub ごとの値として保持する。Windup と Charge の開始時に未解決へ戻す。見た目側は Charge の間だけこれを読む。

**ダメージを受けたとき**(Grub、Spitter 共通のルーチンへの変更):
- Spawning の敵には、プレイヤーの攻撃の判定が当たらない(ダメージも怯みもない)。
- `grub_charger` が Windup、Charge、Recovery の間に攻撃を受けたら、HP だけ減らす。Flinch への遷移も、ノックバックも、状態、方向、残り時間の変更もしない。ノックバックが既存にある場合も、この 3 状態の間は受けない。
- それ以外の状態や敵(Chase の突進型、通常型 Grub、Spitter)は、既存の 0.2 s の Flinch のまま。
- どの状態でも HP が 0 になれば、その時点で倒れる。Windup、Charge 中に倒れたら、同時予告の枠は(導出なので)自動的に空く。レーンと点灯は 0.1 s 以内に消す。

**時間と FPS**: 新しい状態のタイマーはすべて delta で進める。見た目の変化は、状態の経過割合(経過 s ÷ 状態の長さ)から求める。30 FPS と 60 FPS で状態の長さの差は 30 FPS の 1 フレーム(約 0.034 s)以内に収まる。接触は更新ごとのスイープなので、FPS で有無が変わらない。

**プレイヤー側の数値は変更していない(V10)**: この変更は、次のプレイヤー側の数値とコードに一切手を入れない。値は仕様 §1 のまま、既存の実装のままである。
- 攻撃: ダメージ 1、回復 0.35 s。
- ダッシュ: 0.25 s で 4 タイル、ダッシュ中はずっと無敵、クールダウン 0.6 s、ダッシュ中に押した攻撃はダッシュ終了時に出る。
- 被弾: 1 ハート。硬直 0.3 s(入力不可)、被弾から 0.8 s 後まで無敵。
- 無敵のフラグとその 2 つのタイマー(ダッシュの 0.25 s、被弾の 0.8 s)のコードは変えない。変更するのは、新しい突進が問い合わせ関数でフラグを読むことだけ。
- プレイヤーの移動速度、攻撃の届く距離、判定の大きさも変えない。新しい入力ボタンは足さない。

#### 2.3 見た目(段階 0。縮小案は使わない)

色は暫定値(P)。見た目の変形は描画だけに適用し、判定の大きさと位置は変えない。点滅は 1 秒に 3 回以下(単発のフラッシュは可)。

**突進型の目印(常時)**: 通常型と同じスプライトに、背中の熾火の尾根(消灯時 #6B2A1A)を重ねる。出現中から常に見え、Spawning の間は点灯しない。通常型には付けない。

**Spawning(全種類)**: 不透明度を 40% から 100% へ、経過割合に対して線形に上げる。足元に淡い青の輪(#8FB8E8)。赤橙は使わない。

**Windup**(経過割合 p = 経過 s ÷ 0.7):
- 最初の描画で、Grub の中心から固定した方向へ、地面にレーンを出す。長さは 7.0 タイルか壁の手前の短い方(Windup の開始時に、Charge と同じ移動の衝突判定で求める)。幅は敵の接触判定の幅(既存の 1 つの値)と ±0.1 タイル以内で一致させ、実際の判定より広く描かない。
- レーンの描き方: 赤橙(#FF5A1F)の半透明の塗り、明るい縁取り(幅 0.06 タイル)、その外側の暗い下線(幅 0.03 タイル)、1 タイルおきの突進方向のシェブロン(Windup 中は動かさない)。地面の上、キャラクターと弾の下の層で、自己発光(ランタンの明暗の影響を受けない)。Spitter の弾、出現中の表示、他の敵はレーンの上に描く。
- レーンの不透明度: 35% から 100% へ p に対して線形。
- 体: 高さを 100% から 80% へ ease-in、幅を 100% から 108% へ(p に対して)。突進方向と逆に最大 0.15 タイル、スプライトを引く。歩行アニメーションは止める。
- 尾根の点灯: 待機色から赤橙へ p に対して線形。最後の 0.1 s は核色(#FFE3B0)寄りにする。目も赤橙に光る。

**Charge**:
- 体を進行方向に 130%、横に 80% へ伸ばす。核色の芯と赤橙の縁。
- 入る瞬間に 1 回だけ、レーンを 100% 超(核色寄り)の明るさでフラッシュさせる。
- 残像は 0.5 タイル進むごとに 1 つ置き、0.2 s かけて消す(距離で置く)。足元に土煙。
- レーンは 100% に保ち、Grub が通過した後ろ側から消す。前方は残す。Charge の終わりで 0.1 s かけて全部消す。
- 使用済み表示: 接触結果が「抜けた」または「被弾」になったら、芯の明るさを赤橙の暗い側へ落とす。Charge は続く。

**Recovery**: 尾根を 0.1 s で待機色へ戻し、目の光も消す。体全体に沈んだ色(通常色に乗算 #7C8AA0 + 彩度 −40%)を乗せ、高さ 90% に沈める。不透明で、青い輪はない。足元から薄い蒸気を 0.3 s ごとに 1 つ上げる。最後の 0.2 s で高さと色を通常に戻す。

**被弾(Grub が攻撃を受けたとき。突進型のどの状態でも)**: 白いフラッシュ(#FFFFFF、0.1 s、時間で減衰)と小さな火花を当たった位置に出す。位置、向き、大きさ、レーン、点灯は変えない。HP 1 の間、突進型の体に小さな傷の重ね絵を出す(既存の敵の HP 表示はない前提)。

**抜けた合図**: 接触結果が「抜けた」になった更新で、プレイヤーの位置に淡い白青(#CFE8FF)の細い輪を 0.15 s 出す。「被弾」のときは出さず、既存の被弾表現だけを使う。

**音**: 実装しない。粒子(残像、土煙、蒸気、火花)は新規の 1 種を足す。

#### 2.4 開発用補助(開発ビルド限定。リリースビルドには含めない。プレイヤー向けの入力は足さない)

- 部屋の選択(1〜5)。
- 部屋ごとの突進スイッチのオン/オフの切り替え。
- 30 FPS と 60 FPS の切り替え。
- 状態の遷移ログ: 時刻(ゲーム内の経過時間)、敵の ID と種類、遷移前後の状態、突進方向、接触結果(未解決 / 抜けた / 被弾)、波の出現(波番号、スロット、「遠い方」の選択結果)、Windup の開始時のプレイヤーとの距離。D-009 に合わせて、「波 N の全員が出現中に入った時点(K と T の調べ始め)」もログに出す。
- **今回足したログ項目**: 突進型の Recovery の終了時刻(Chase に戻った時刻)。次の Windup の開始時刻との差が 2.5 s 以上であることを、ログから読めるようにするため。

### B. Handoff 28 との差分

1. **2.2 Chase → Windup の条件 1**: 起点を「前回の Recovery が終わって Chase に戻った時点」と明記した。「Charge の終了ではない」「Recovery の 0.8 s は 2.5 s に含めない」を追記し、数値の例(t+3.3 以降)を足した。Handoff 28 の文面も Recovery 終了後だったので、数値は変わらない。文面を具体的にしただけ(F-1)。
2. **2.1 Grub 速度**: 部屋 1〜5 の数値(2.0 / 2.0 / 2.2 / 2.2 / 2.4)を表のほかに列挙した。通常型と突進型の Chase の速度に使い、Charge の 8.0 とは別と書いた(V7 未確認 1)。2.2 の Chase の動きの欄にも「部屋の Grub 速度」と書いた。
3. **2.1「FL / FR のうち遠い方」**: 距離を「それぞれ中心間」で比べる、「2 つの距離が等しいときは FL」と明記した(V7 未確認 2)。仕様 §4.1、D-005 と同じ内容で、規則の追加ではない。
4. **2.1 出現位置の待ち**: 「同じ波の複数のスロットの待ちは、波の出現を決めた時点から同時に始まる」を独立した 1 文にして強調した(V12(c) の補足)。Handoff 28 にも同じ内容が含まれていた。
5. **2.2 末尾**: 「プレイヤー側の数値は変更していない」の節を新設した。攻撃の回復 0.35 s、ダッシュの 0.25 s・4 タイル・クールダウン 0.6 s、被弾の硬直 0.3 s・無敵 0.8 s、無敵フラグと 2 つのタイマーのコードに触れないことを列挙した(V10)。Handoff 28 は「プレイヤー側の数値やキットの変更は含めない」とだけ書いていた。
6. **2.4 開発ログ**: Recovery の終了時刻を足した(F-1 を確認しやすくするため)。
7. 変更なし: 2.3 の見た目のすべて。波、K/T、構成、接触の定義、怯みの規則。欠陥 D の扱い(触れない、原因を推測しない)。

### C. 模擬上の前提が残る項目(Handoff 17 の番号。Handoff 28 から変更なし)

実コードで確認済みではない。`sim/repo-notes.md` にはスポナー、部屋、波、出現位置、出現中の記述がない。

| # | 項目 | 結果 |
|---|---|---|
| 1 | 部屋データ、スポナー、波(敵の一覧で数える、スロットごとの待ちタイマー、全員が出現中に入った判定を 1 か所に置く) | 模擬上の前提 |
| 2 | 部屋のコードと敵コントローラの分離、部屋の終了条件と波の結合の強さ | 模擬上の前提 |
| 3 | 接触の判定形状と大きさ、レーン幅の元の値 | 模擬上の前提 |
| 4 | Spitter の弾(壁で消える、敵を通り抜ける) | 模擬上の前提 |
| 5 | 視覚の仕組み(必須要素 1〜6 が使える、敵の HP 表示がない、粒子を新規に足す。レーンの赤橙と弾・ランタンの色の近さは未確認) | 模擬上の前提 |
| 7 | 既存の敵の他のタイマー(噛みつきの間隔など)が delta で進んでいるか | 一部確認 / 一部模擬上の前提(delta、30/60 FPS、Flinch 0.2 s、無敵 0.25 s と 0.8 s は `sim/repo-notes.md` で確認) |

- 項目 6(接触結果の通知)は前提ではなく、この変更で足すもの。
- 前提が外れた場合の戻し先は、Handoff 17 と D-007 の 2 のとおり。
- スロット座標の実数値は不明のまま。各部屋で仕様の意味(奥、左右の側面、奥の左右の隅)に対応する位置にあるとして扱う。「遠い方」は、この座標の中心間距離で比べる。

### D. 実装していない・確認していないこと

- コードの変更、ビルド、テストの作成と実行は行っていない(D-008)。この文書は変更内容の記述だけである。
- 実機のゲームパッドの操作感、0.7 s の予告を読んでダッシュまで入力できるか、暗い床や小さい画面での読み取り(H1〜H4)は確認していない。
- 欠陥 D(被弾直後のダッシュ中のダメージ)には触れておらず、原因は推測していない。規則は `game-designer` が決める事項で、この Step では変更していない。
- 2 体の突進型が同じ更新で Windup の条件を満たす場合の順序は、既存の敵の更新順で決まる。仕様に規則がなく、この変更も規則を足さない。V5 には影響しない。
- 音、新しい入力ボタン、Spitter の変化、新しい敵は含めない。
- 仕様の欠落や矛盾は見つからなかった。`outcome: question` にする必要はない。

## Decisions already made

- D-001: 攻撃とダッシュのみ。新ボタンなし。
- D-004: 技術方針(共通コントローラへの状態追加など)。
- D-005: 怯み、接触の解決、「遠い方」(同距離は FL)。
- D-007: 前提の台帳。確認できない項目は「模擬上の前提」と明記する。
- D-008: Build は変更内容を正確に書いた時点で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- すべての結果は模擬ビルドに基づく(D-008)。実機の証拠ではない。
- 仕様と数値は変えていない。新しい入力ボタンなし。プレイヤー側の数値は変えていない。
- 欠陥 D の原因は推測しない。

## Open questions

- なし。Handoff 31 の 3 つの問いには、上の「0. 確認結果」で答えた。
- 再検証で、模擬ビルドが再び突進の再開始の起点を Charge の終了と書いた場合は、記述が仕様と一致していても起きたことになる。その場合の原因は、変更内容の記述からは判断できない。Studio が扱いを決める。

## Expected output

Studio は、A(修正後の 2.1〜2.4)と B(差分)を使って Verify の Handoff を組み直し、`qa` に F-1、V7、V10、V12(c) の再検証を依頼する。2.3 は `art-director` 向け。`qa` には Sender assessment を渡さない。

## Sender assessment

- 確信度: 数値と規則はすべて `design/combat.md` §1、§3.3、§4.1、§4.3 と D-005、D-009 から写した。仕様との対応は高い。
- F-1 について: Handoff 28 と `sim/repo-notes.md` はともに「Recovery が終わってから」と書いていた。模擬ビルドの食い違いが記述の曖昧さによるものとは言い切れない。文面を具体的にして再検証に出すのが、この Step でできる範囲である。
- Grub 速度についても同様で、Handoff 28 の表には数値があった。列挙を足したのは確認しやすくするためで、数値は変えていない。
- 低いのは、台帳 1〜5 の模擬上の前提と、見た目の細部(レーン長の求め方、使用済み表示の描き方)。変更はない。
- 範囲外は広げていない。欠陥 D の原因の推測は書いていない。

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md、sim/build-0.4.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/31-studio-to-gameplay-engineer.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END
