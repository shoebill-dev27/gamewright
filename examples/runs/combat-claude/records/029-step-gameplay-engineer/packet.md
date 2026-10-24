# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/25-studio-to-gameplay-engineer.md
next_seq: 26

## You may write

- goals/G-001-combat-monotony/26-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/25-studio-to-gameplay-engineer.md
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
# Simulated repository notes — lantern-depths (build 0.3)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data
  (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it
  is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on
  overlap. There is no concept of blocking or facing yet.
- Player invulnerability: one on/off flag. The dash switches it on and starts a 0.25 s timer;
  getting hit switches it on and starts a timer that ends 0.8 s after the hit. Each timer switches
  the flag off when it ends.
- Movement: simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.

<!-- dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
if a Role writes it into a Handoff. -->
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

<<<FILE decisions/D-008-owner-simulated-build-judgment.md
---
kind: decision
id: D-008
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-008: Build は変更内容を Handoff に正確に書いた時点で完了とし、Goal は模擬ビルドに基づいて判定する(Escalation 20 の Option C)

## Decision

Owner は Escalation 20 の Option C を選んだ。Owner の言葉:

> Cで進めてください。このプロジェクトは模擬専用のサンプルなので、sim/repo-notes.md をコードとして扱い、Build は変更内容を Handoff に正確に書いた時点で完了とします。模擬ビルドは私ではなくランタイムのシミュレーターが、その変更内容から作ります。結果には模擬であることを明記したうえで、Goal の判定は模擬ビルドに基づいて行ってください。

内容と条件:

1. `sim/repo-notes.md` を、このプロジェクトのコードとして扱う。D-007 の台帳 7 項目は、その記述に照らして確認する。記述が答えない項目は「模擬上の前提」と明記する。
2. Build(`gameplay-engineer`)は、変更内容を Handoff に正確に書いた時点で完了とする。実際のコードの変更、ビルド、テスト実行は行わず、行ったとも書かない。
3. 模擬ビルドは、Owner ではなくランタイムのシミュレーターが Build の変更内容から作る。Studio は模擬ビルドを自分で書かない。変更内容は、シミュレーターが観察可能な挙動(数値、時間、部屋の構成、状態遷移、視覚要素)を導けるだけの精度で書く。
4. Verify・Play・Review は模擬ビルドに対して行い、Goal の判定も模擬ビルドに基づいて行う。すべての成果物(報告、Review、Outcome)に「模擬ビルドに基づく」ことを明記する。
5. 限界(Studio の追記。Owner の条件の実施方法): この判定は模擬の証拠に基づく。ゲームパッドの操作感、0.7 秒の予告で足りるか、暗い床での読み取りやすさ(H1〜H4)は、実機では確認されない。Outcome にその旨を書く。

D-001〜D-007 は変わらない。新しい入力ボタンもビジョンの柱の変更もない。D-007 の 7(コードが読めない場合は返す)は、`sim/repo-notes.md` を読める入力として渡すことで入力の欠落が解消したため、今回は適用しない。

## Rationale

プロジェクトは `repository: none` の模擬専用サンプルで、Owner がその前提で工程を最後まで進めることを選んだ。Goal の判定を模擬ビルドに基づかせるのは、Owner の価値判断(Escalation 20 が Goal の再解釈に当たるとした点)であり、Studio は覆さない。

## Alternatives considered

- Option A(実リポジトリの提供): リポジトリがないため選ばれなかった。
- Option B(計画と基準の確定までに縮小): Owner が工程を最後まで進めることを選んだ。

## Revisit when

実際のゲームのコードベースが用意された場合。そのときは模擬の結果を実機の証拠として扱わず、Build と Verify を実コードでやり直すかを Owner に確認する。
>>>END

<<<FILE decisions/D-007-build-without-code-access-assumption-register.md
---
kind: decision
id: D-007
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-007: コードを読めない状況では、T0 を「前提の台帳」に置き換え、前提ごとに検出点と戻し先を決めて Build を進める

## Decision

D-004 の技術方針(状態の追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ)は変えない。D-004 の「T0 で確認する前提」の扱いだけを次のとおり改める。

1. **T0 の扱い**: T0 を、着手前に済ませる独立した調査工程としては扱わない。未確認の 7 項目は「前提の台帳」(Handoff 16 の Findings)に載せ、各項目を、それに最初に依存するタスクの冒頭で確認する(プローブ)。確認できた事実は Build の Handoff に書く。
2. **前提が崩れたときの戻し先**: 崩れた時点で、そのタスクを止めて返す。分類は次のとおり。
   - (i) D-004 の範囲内の局所的な修正で済む: Build が直して進め、Handoff に記録する。
   - (ii) 仕様の変更が要る: `game-designer` へ。
   - (iii) 技術方針の変更が要る(D-004 の「Revisit when」に該当する場合を含む): `technical-director` へ。
   - (iv) 必須の視覚要素が実現できない: `art-director` へ(Studio 経由)。
3. **推測の封じ込め**: 未確認の前提に依存するコードは、1 か所の継ぎ目(関数または定数)の後ろに置く。前提が外れたときの修正を局所にするため。
4. **報告の規則**: Build は、実行できなかった確認を「通った」と書かない。確認できたこと、できなかったこと、その理由を分けて書く。
5. **無敵の問い合わせ関数**: 署名(1 つの真偽で答える)は変えない。無敵フラグを書くタイマーのコードには、この Build では触れない(欠陥 D は別扱い)。
6. **接触結果の通知**: D-004 の「見た目への口」に、突進ごとの接触結果(未解決 / 抜けた / 被弾)を加える。接触を解決する 1 つの関数が決めた値を、その突進の間だけ保持する。突進の開始時に未解決へ戻す。
7. **打ち切りの条件**: Build が、読める・書けるコードが全くないために、台帳のプローブもコード変更もできないと再び報告した場合、それは前提のリスクではなく入力の欠落である。この場合は Build を再試行せず、`technical-director` に返し、Owner へのエスカレーション(リポジトリの提供、または模擬の範囲の確認)を用意する。

この決定が扱わないこと: 戦闘の規則・数値、D-001〜D-006 の内容。欠陥 D の原因と修正。

## Rationale

- D-004 の方針は、`sim/repo-notes.md` の確認済みの 7 つの事実と矛盾しない。確認できた事実(共通コントローラ、状態遷移、可変 delta、1 つの無敵フラグ)が方針の骨格を支えている。崩れると方針が変わるものは、未確認の項目のうち、部屋の終了条件の結合の強さと判定形状の 2 点で、どちらも実装の入口で見える。
- 同じ入力を与えれば T0 の結果は変わらない。事前に別の調査をしても情報は増えない。実装の入口で確かめれば、確認とコード変更を同じ場所で行える。
- 継ぎ目を 1 か所にすると、前提が外れても、書き直しの範囲が 1 か所で済む。
- 接触の解決はすでに 1 つの関数にまとめる方針(D-004)なので、結果を保持する費用は小さい。仕様と D-006 は、この通知を「望ましい(S)」とし、省いてよいとしている。
- 打ち切りの条件を先に決めておくと、コードが全くない状態でのやり直しを繰り返さずに済む。

## Alternatives considered

- **(b) 仮定で埋めた計画に作り直し、対象を縮める**: 仮定が正しいかどうかは実装の入口でしか分からない。先に縮めると、不要な縮小で仕様の効果(波、予告)を落とすおそれがある。採らない。縮小は、前提が実際に崩れた箇所に限る。
- **(c) 今すぐ Owner に確認する**: このサンプルは `repository: none` で、ビルドを `sim/` で模擬する設計である。Build が何も作れないと分かる前にエスカレーションするのは早い。ただし、7 の条件に当たった時点で行う。
- **T0 を台帳なしで保留する**: 崩れたときの戻し先がなく、Build がまた止まる。採らない。

## Revisit when

- Build が、台帳の項目 1(部屋)または項目 3(判定形状)で D-004 の「Revisit when」に該当する事実を見つけた場合。
- Build が、実行できる確認がほとんどなく、報告が「未確認」ばかりになる場合(7 の条件)。
- 欠陥 D の修正が、問い合わせ関数の前提を変える場合(D-004 と同じ)。
>>>END

<<<FILE goals/G-001-combat-monotony/24-game-designer-to-studio.md
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
