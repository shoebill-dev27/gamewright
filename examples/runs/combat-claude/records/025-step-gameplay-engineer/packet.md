# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/21-studio-to-gameplay-engineer.md
next_seq: 22

## You may write

- goals/G-001-combat-monotony/22-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/21-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 21
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 21: studio → gameplay-engineer — 変更内容を正確に書く(模擬ビルドの元になる Build)

## Task

承認済みの仕様と計画に従い、`sim/repo-notes.md` をこのプロジェクトのコードとして扱って、ゲームに加える変更内容を Handoff に正確に書く。変更内容を正確に書いた時点で、この Build は完了する(D-008)。

## Context

G-001「戦闘が単調なので改善したい」。方向は D-002(部屋の構成と進行が主軸、予告つき Grub 突進を併用)で、仕様は `design/combat.md`(D-003、D-005)と `design/grub-charge-telegraph.md`(D-006)、技術方針は D-004 と D-007 で決まっている。以前の Build は実コードがなく 2 回 `question` で返った(Handoff 14、18)。Owner は Escalation 20 に Option C で回答した(D-008): `sim/repo-notes.md` をコードとして扱い、模擬ビルドは変更内容から、ランタイムのシミュレーターが作る。以後の Verify・Play・Review は模擬ビルドに基づく。

## Findings

- 入力の欠落は解消した。`sim/repo-notes.md` は読める入力として Load にある。D-007 の 7(コードが読めない場合に返す)は今回は適用しない。
- 台帳 7 項目(Handoff 17、D-007)は `sim/repo-notes.md` と `sim/build-0.3.md` に照らして確認する。記述が答える項目は、答えの引用つきで「確認(模擬のコード)」と書く。記述が答えない項目は「模擬上の前提」と書き、その前提を変更内容に明記する。実際のコードで確認済みとは書かない。
- 範囲: D-002/D-003 の部屋の構成と進行(波、突進スイッチ)、予告つき Grub 突進、D-006 の視覚要素、D-004 の接触結果の通知(視覚仕様の要素 9)、D-005 の規則(怯まない 3 状態、接触は突進ごとに最初の重なりで 1 回だけ、遠い方は出現を決める時点で選ぶ)。
- 範囲外: 欠陥 D(被弾直後のダッシュ中のダメージ)の修正、新しい入力ボタン、Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更。

## Decisions already made

- D-001: 攻撃とダッシュのワンボタン戦闘。新ボタンなし。
- D-002: 主軸は部屋の構成と進行。併用は予告つき Grub 突進の 1 つだけ。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。部屋は突進スイッチで外せる。
- D-004: 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ。
- D-005: 突進型は 3 状態で怯まない。接触は突進ごとに最初の重なりで 1 回だけ。「遠い方」は出現を決める時点で選ぶ。
- D-006: 突進の予告は地面のレーン + 熾火の点灯 + 沈み込み。赤橙は害になる状態だけに使う。
- D-007: 台帳 7 項目と、前提が崩れたときの戻し先。
- D-008: Owner が Option C を選んだ。変更内容の記述で Build 完了。結果に模擬であることを明記する。

## Constraints

- 変更内容は、シミュレーターが観察可能な挙動を導ける精度で書く。部屋ごとの構成(敵の種類と数、波、出現位置、突進スイッチ)、時間の値(予告 0.7 秒などの仕様の数値)、状態と遷移、視覚要素、接触結果の通知、30/60 FPS で同じ挙動になる扱いを含める。
- 仕様の数値を勝手に変えない。仕様が曖昧、矛盾、または欠落している場合は決めず、`outcome: question` で返す(Studio が `game-designer` に回す)。
- 実行していないことを実行したと書かない。ビルド、テスト、動作確認は行っていない。受け入れ基準については「どの変更で満たす想定か」の対応表を書き、満たしたとは書かない。
- 模擬ビルドを自分で書かない。それはシミュレーターの仕事で、この Build の成果物ではない。
- 開発用補助(部屋の選択、突進スイッチ、30/60 FPS 切り替え、状態の遷移ログ)は D-004 のとおり開発ビルド限定で、プレイヤー向けの入力は足さない。
- 欠陥 D の原因に結び付く推測は書かない。

## Open questions

- 台帳 7 項目のうち、`sim/repo-notes.md` が答えない項目はどれか。その場合の模擬上の前提は何か。
- 視覚仕様の必須要素 1〜6 と要素 9 は、`sim/repo-notes.md` の記述にある仕組みで足りるか。

## Expected output

次の Handoff を `goals/G-001-combat-monotony/22-gameplay-engineer-to-studio.md` として書く。`to: studio`(Verify で `qa` と `art-director` を並列にするため、Studio が受け手ごとに新しい Handoff を組む)。`outcome: done`(曖昧さがあれば `question`)。

Findings に次を書く:

1. 台帳 7 項目の結果(確認(模擬のコード)/ 模擬上の前提)。
2. 変更内容(部屋ごと、敵コントローラ、スポナー、視覚要素、接触結果の通知、開発用補助)。シミュレーターがそのまま読める形で。
3. 受け入れ基準と変更の対応表。
4. 実装していない・確認していないことの一覧(実行、ビルド、テスト、実機の感触)。

自己評価(確信度、疑い)は `## Sender assessment` に分けて書く。`qa` と `playtester` には渡されない。

## Sender assessment

(Studio が書いた routed Handoff のため、なし。)

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md、sim/build-0.3.md、project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md、decisions/D-002-combat-direction-rooms-and-grub-charge.md、decisions/D-003-grub-charge-and-room-rules.md、decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-006-grub-charge-telegraph-visual.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
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

状態: G-001 / D-002 / D-003 / D-005 に基づく仕様。**この文書の新しい数値はすべて暫定値(P)**。H1〜H4(ゲームパッドの操作感、各部屋の実時間、音と演出、敵の速度と弾速など)の実機確認後に調整する。確認前に、プレイヤー側の数値は変えない。

変更履歴: Handoff 10 / D-005 で、怯み(§2.1、§8)、接触の定義(§3.4、§3.5、V3、V4、V11)、遠い方のスロットの規則(§4.1、§4.3)、波の既定(§4.1)を明記した。数値は変えていない。

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
- 出現位置(スロット): 扉側(Door)、奥(Far)、左側面(L)、右側面(R)、奥の左隅(FL)、奥の右隅(FR)。実際の座標は部屋データ。
  - 出現の時点でプレイヤーがスロットから 4 タイル未満なら、出現を最大 2.0 s 待つ。2.0 s たったら、そのまま出現中に入る。
  - **出現位置にプレイヤーが重なっても、押し出さない**。出現中の 0.8 s は無害で、見えるので動ける。待ちは最大 2.0 s(上のとおり)。
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
- V7: 部屋 1〜5 の波の構成、条件(K, T)、Grub 速度、Spitter 間隔が §4.3 の表と一致する。部屋 3 と 5 の波 2 の Spitter が、§4.1 の規則(出現を決める時点で遠い方、同距離は FL、待ちの間は選び直さない)で選ばれる。「T s」の起点は最後の敵の出現中の終わり、「生きている敵」には出現中の敵を含む(§4.1)。
- V8: 出現中が 0.8 s。この間は行動もダメージもない。出現位置にプレイヤーが重なっても押し出されず、出現中は無害。
- V9: Spitter の最初の 1 発が出現中の終了から 1.0 s、弾速 4.0 タイル/s。弾は壁で消え、敵を通り抜ける。
- V10: プレイヤー側の数値(攻撃、ダッシュ、被弾の規則)が変わっていない。
- V11: 突進型 Grub の Windup、Charge、Recovery の間に攻撃を当てると、HP は減るが、状態、方向、残り時間は変わらない(怯まない)。HP が 0 になれば、その時点で倒れる。Chase 中に攻撃を当てると 0.2 s の怯みに入り、Chase に戻る(既存)。出現中は攻撃を当ててもダメージを受けない。

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

(1〜3 の回答は Handoff 08 にある。怯み、接触の定義、遠い方の規則は D-005 で決定済み。)

## 10. art-director に渡す条件

見た目の具体案は art-director が決める。仕様として求める条件:

- **突進の予告**: Windup の 0.7 s の間ずっと見える。突進が来ることと、その方向がわかる。通常の Grub の歩きと見分けがつく。色だけに頼らない。音だけに頼らない。音を付ける場合は、Windup の開始に合わせる。
- 長さは時間(0.7 s)で決まり、30 FPS と 60 FPS で同じ長さに見える。
- Charge 中は、歩きや Windup と見分けがつく。Recovery 中は、「止まっていて攻撃が通る」とわかる。
- 突進型は Windup、Charge、Recovery の間、攻撃を受けても怯まない。攻撃が当たったことは、HP の減少が見えれば足りる(怯みの動きで示さない)。
- 突進の予告が、Spitter の弾、出現中の表示、他の敵の動きと重なっても、読める。
- 出現中(0.8 s)が、行動する敵と見分けがつく。
- 突進型の Grub が、出現時から通常型と見分けがつくかどうかは、art-director が判断する。

## Rooms(旧記述)

旧: 5 部屋、各 3〜6 体、Grub と Spitter の混成。部屋は全敵撃破で終わる。→ §4 に置き換え。

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/grub-charge-telegraph.md
# Grub 突進の予告の見た目(視覚仕様、暫定)

状態: G-001 / Handoff 11 に基づく art-director の視覚仕様。色、割合、長さの新しい値はすべて暫定値(P)。実機(ゲームパッド、小さい画面、30/60 FPS)での読み取りは Play で確認するまで未確認。
戦闘の規則と数値(予告 0.7 s、突進 8.0 タイル/s・7.0 タイル、Recovery 0.8 s、出現中 0.8 s、接触の定義、怯みの規則)は `design/combat.md` と D-003〜D-005 のとおりで、この文書は変えない。決定の記録は D-006。

## 1. 意図

突進型 Grub は、「止まって、体を沈め、熾火(おきび)が灯り、足元に赤橙の帯が伸びる」ことで、害の前に突進を知らせる。帯が突進の方向と通る範囲そのものを示すので、プレイヤーは「その線から出る」か「当たる直前にダッシュで抜ける」を選べる。突進の後は、熾火が消えて沈んだ体で隙を読ませる。予告は色だけに頼らず、形(帯と矢印)・動き(沈み込み)・明るさ(熾火と帯の強さ)の組み合わせで伝える。

## 2. 共通ルール

- 見た目のタイミングはすべて、状態の経過時間の割合(経過 s / 状態の長さ)から求める。フレーム数や更新回数に結び付けない。30 FPS と 60 FPS で同じ長さに見える。これは §10 の「長さは時間で決まる」条件を満たすためである。
- 見た目の変形(拡大縮小、ずれ)は描画だけに適用する。判定の大きさと位置は変えない。
- 敵が攻撃を受けたことは、白い被弾フラッシュ(§8)だけで示す。怯みの動き(のけぞり、縮み、位置のずれ)を予告や状態の表示に使わない。
- 点滅は 1 秒に 3 回以下にする。単発のフラッシュは可。
- 脅威色(赤橙)は、「これから害になる、またはいま害になる」ことだけに使う。無害な状態(出現中、Recovery)には使わない。
- 色の指定(暫定値、P):
  - 脅威の赤橙: #FF5A1F
  - 熱い核: #FFE3B0
  - 熾火の待機色(消灯時の突進型の目印): #6B2A1A
  - Recovery の沈んだ色: 通常色に乗算 #7C8AA0 + 彩度 −40%
  - 出現中の淡い青: #8FB8E8
  - 被弾フラッシュ: #FFFFFF
  - 抜けた合図: #CFE8FF
  - 既存の Spitter の弾の色、ランタンの色との差は未確認。T0 で確認し、近ければ値だけを変える(形で区別する設計は変えない)。

## 3. 突進型の目印(常時)

- 突進型 Grub は、通常型と同じスプライトに、背中の「熾火の尾根」(暗い赤茶 #6B2A1A、点灯していない炭のような見た目)を重ねて区別する。出現中から常に見える。
- 尾根は暗い色にとどめ、通常の歩行中は脅威の赤橙を使わない。これは Windup の点灯との対比を最大にするためである。
- 尾根が「何を意味するか」は、部屋 2 で突進を見て学ぶ。目印を最初から見せることで、部屋 4、5 でどの Grub が突進するかを先に読める。
- 通常型の見た目は変えない。

## 4. 出現中(Spawning、0.8 s)

- 突進型でも通常型でも、体は半透明(不透明度 40%→100% に、時間で線形に上がる)で、足元に淡い青(#8FB8E8)の輪が出る。赤橙は使わない。
- 出現中は動かず、攻撃も通らない。Recovery(不透明、蒸気あり、§7)と、半透明と青い輪で見分ける。
- 突進型の尾根は出現中も見えるが、点灯しない。

## 5. Windup(予告、0.7 s)— 主役

### 5.1 突進の線(レーン)

- Windup の開始の最初の描画で、Grub の中心から固定した方向へ、地面に帯(レーン)を出す。方向はレーンの向きで示す。
- 長さ: 7.0 タイル、または壁まで(短い方)。壁の手前で切る。
- 幅: Grub の既存の接触判定が通る範囲と一致させる(±0.1 タイル)。実際の判定より広く描かない(広く描くと「当たらないのに避けた」になり、窓の読みを狂わせる)。
- 見た目: 赤橙(#FF5A1F)の半透明の塗りと、1 本の明るい縁取り(幅 0.06 タイル)、1 タイルおきに突進方向を指す矢印(シェブロン)。シェブロンは Windup 中は動かさない(動くと突進が始まったと誤読されるため)。
- 層: 地面の上、キャラクターと弾の下。ランタンの明暗の影響を受けず、暗い床でも読める明るさにする(自己発光)。縁取りの外側に暗い下線(幅 0.03 タイル)を引く。
- 明るさの変化: 不透明度を 35% から 100% へ、Windup の経過時間に対して線形に上げる。最初の描画から 35% で完全な形が見えている。Windup の終わりが近づくほど強くなり、突進の瞬間が近いことを示す。
- Charge に入る瞬間: 1 回だけ 100% を超える明るさ(核色 #FFE3B0 寄り)にフラッシュする。

### 5.2 体

- 体を沈める: 高さを 100%→80% に、Windup の経過時間に対して ease-in で縮める(幅は 100%→108%)。見た目だけで、判定は変えない。さらに、突進方向と逆に最大 0.15 タイル、スプライトを引く(反動)。
- 熾火の点灯: 尾根の色を待機色から赤橙へ、経過時間に対して線形に点灯させる。最後の 0.1 s は核色に寄せる。
- 目も同じ赤橙に光る。
- 歩行アニメーションは止める。止まった Grub に熾火とレーンが付いている、が合図の組み合わせ。通常の歩きとは、止まる・沈む・光る・レーンが出るの 4 点で区別できる。
- 音(予定範囲に音があれば): Windup の開始に合わせ、0.7 s で音程が上がる短い溜め音。音がなくても読める設計とする。

### 5.3 重なり

- Spitter の弾、出現中の表示、他の敵はレーンの上に描く。レーンの縁取りと矢印は、弾の下でも一部が見える。
- 同時にレーンが出るのは 1 本まで(規則どおり)。
- 倒された、またはポーズなどの場合: 倒された時点でレーンと点灯を 0.1 s 以内に消す。ポーズ中は全部の変化が止まる。

## 6. Charge

- 体を進行方向に伸ばす(進行方向 130%、横 80%)。核色の熱い芯と、赤橙の縁。
- 残像: 0.5 タイル進むごとに 1 つの残像を置き、0.2 s かけて消す(距離で置くので FPS に依存しない)。足元に土煙。
- レーン: 100% に保ち、Grub が通過した後ろ側から消していく。前方は残る。
- Charge の終わりでレーンを 0.1 s で消す。
- 接触が解決した後の「使用済み」表示(望ましい。§9 の口が使える場合): 接触が解決したら、核色を赤橙の暗い側に落とす(芯が弱まる)。Charge は続くが、その突進はもう害を与えないことを示す。「重なったのに当たらない」違和感を減らすための合図。口が使えなければ省く。
- 被弾フラッシュ(§8)は Charge 中も同じ。怯まないので、動きは止まらない。

## 7. Recovery(0.8 s)— 隙

- 突進は終わった、いまは止まっていて攻撃が通る、と読ませる。
- 熾火を消す(尾根は待機色へ 0.1 s で戻る)。目の光も消す。体全体に沈んだ色(§2)を乗せる。体は高さ 90% に沈み、足元から薄い蒸気が 0.3 s ごとに 1 つ上がる。
- 最後の 0.2 s で、体が 100% の高さに戻り、色も通常に戻る。隙が終わる合図。
- 出現中との区別: Recovery は不透明で、青い輪がなく、蒸気がある。
- 留意: 沈んだ見た目が「死にかけ」「無敵」と誤読されないか(未確認、Play で確認)。誤読された場合は、蒸気を強め、沈んだ色を弱める。
- 音(あれば): 低い息の抜ける音 1 回。

## 8. 被弾(Grub が攻撃を受けたとき)

- どの状態でも同じ。白いフラッシュ(#FFFFFF、0.1 s、時間で減衰)と小さな火花を、当たった位置に出す。
- 位置、向き、大きさ、状態の演出(レーン、点灯)は変えない。怯みに見える動きは付けない。
- HP が減ったことが分かること: 既存の敵の HP 表示があればそれを使う。なければ、HP 1 の間は体に小さな傷の重ね絵を表示する(小アセット 1 つ)。

## 9. 抜けた合図(望ましい)

- 接触の瞬間にプレイヤーが無敵で、ダメージなしに解決されたとき: プレイヤーの位置に、淡い白青(#CFE8FF)の細い輪を 0.15 s 出す。害を与えた場合の既存の被弾表現とは別の形にする。
- 被弾した場合は既存の被弾表現だけを使い、抜けた合図は出さない。
- 必要な情報: 接触の解決結果(無敵で抜けた/被弾)。D-004 の「見た目への口」にこれが含まれない場合は、この合図と §6 の使用済み表示を省く。省いても必須の予告は成立する。

## 10. 受け入れ基準

### 10.1 検証用(qa 向け、30 FPS と 60 FPS の両方)

- A1: Windup の最初の描画からレーンが出ている(不透明度 35% 以上)。予告のない Charge はない。出現直後、Recovery 後、被弾中、ポーズ復帰後を含む。
- A2: レーンの向きが、Charge の実際の進行方向と一致する(角度の差 ±3° 以内)。Windup 中にプレイヤーが動いても変わらない。
- A3: レーンの幅が接触判定の範囲と ±0.1 タイル以内で一致する。長さは 7.0 タイルまたは壁の手前まで。
- A4: レーンの不透明度が Windup の間、35%→100% に単調に上がる。30 FPS と 60 FPS で、同じ経過時間における値の差が 5% 以内。
- A5: 最も暗い床の上で、Windup の開始時点(不透明度 35%)のレーンの縁と床の明るさの比が 3:1 以上。
- A6: 沈み込み、熾火の点灯が Windup の 0.7 s の間(±1 フレーム(30 FPS 基準))に完了する。
- A7: Windup、Charge、Recovery の間に攻撃を当てても、位置、大きさ、レーン、点灯、状態の演出が変わらない。白いフラッシュと火花だけが出る。
- A8: Windup 中に倒すと、レーンと点灯が 0.1 s 以内に消える。ポーズで全部が止まり、復帰で続きから再開する。
- A9: Spitter の弾がレーンの上にあるとき、弾はレーンの上に描かれ、レーンの縁と矢印の一部が見える。
- A10: 出現中(半透明、青い輪)、Windup(レーン、熾火)、Charge(伸びた体、残像)、Recovery(沈んだ色、蒸気)、通常の歩きの 5 つの見た目が、1 枚のスクリーンショットで互いに区別できる。
- A11: 突進型の尾根が、出現中を含む全状態で見える。通常型には付かない。
- A12: 突進スイッチをオフにすると、尾根、レーン、その他の突進の演出は一切出ない(通常型と同じ見た目)。
- A13: 抜けた合図(§9)を実装した場合、無敵で抜けたときにだけ出て、被弾したときには出ない。

### 10.2 体験の観点(Play と Review 向け。Playtester の handoff には書かない)

- 突進型の Grub を初めて見たとき、「何かが来る」と分かるか。当たったとき、「予告は見えていた」と言えるか。
- 暗い部屋、小さい画面、ゲームパッドの操作中でも、レーンの向きと範囲が一瞬で読めるか。
- レーンと Spitter の弾を、形で見分けられるか(どちらも赤橙系だが、帯と小さな丸)。
- Windup 中の Grub が「まだ無害」と読めるか。近づいてよいと感じさせすぎないか。
- ダッシュで抜けたとき、「抜けた」と感じられるか。
- Recovery を「攻撃のチャンス」と読めるか。「死にかけ」や「無敵」と誤読されないか。
- 攻撃しても止まらないことが、「止められない突進」として自然に読めるか。
- 30 FPS と 60 FPS で同じに感じられるか。
- 色覚の差で、レーンの形と沈み込みだけで読めるか。

## 11. 必要な視覚要素(gameplay-engineer 向け)と見立て

優先度: 必須(M)、望ましい(S)、あれば(N)。

| # | 要素 | 優先 | 新アセット | 既存の仕組みで足りるか(T0 で確認) |
|---|---|---|---|---|
| 1 | 状態、経過割合、突進方向の取得 | M | なし | D-004 の「見た目への口」 |
| 2 | レーン(帯、縁取り、矢印) | M | 小(矢印の 1 タイル分、または手続き描画) | 地面層に半透明の矩形を、色と不透明度を指定して描けるか |
| 3 | スプライトの色変調、拡大縮小、描画ずらし | M | なし | Windup の沈み込みと Charge の伸びに必要。なければ変形なしで色と明るさだけに縮める案を下記に示す |
| 4 | 熾火の尾根の重ね絵 | M | 小(重ね絵 1 枚。向きが複数なら向きごと) | 重ね描きができなければ、体の縁の色変調で代用 |
| 5 | 被弾フラッシュ | M | なし | 既存の被弾の白フラッシュがあれば流用 |
| 6 | 出現中の半透明と青い輪 | M | 小 | 既存の出現演出があれば色を調整 |
| 7 | 残像、土煙、蒸気 | S | 小(粒子 1 種) | 既存の粒子があれば流用。なければ省いても必須は成立 |
| 8 | 傷の重ね絵(敵に HP 表示がない場合) | S | 小(1 枚) | 既存の HP 表示を確認 |
| 9 | 接触の結果(抜けた/被弾)の通知 | S | なし | 口にない場合は §6 の使用済み表示と §9 を省く |
| 10 | 音(溜め音、息の音) | N | 音 2 つ | 音が予定範囲にある場合のみ |

- 新しい大きなアセットは必要ない。小さな新規素材は、矢印 1 枚、尾根の重ね絵、必要なら傷の重ね絵と粒子 1 種で、既存の Grub のスプライトに重ねる。
- 要素 3 が使えない場合の縮小案: 変形なしで、Windup の沈み込みの代わりに尾根と目の点灯とレーンだけで予告する。Recovery は色変調と蒸気で示す。予告の成立は、色だけでなく、レーンの形と点灯の組み合わせで維持する。
- 要素 2 が難しい場合の代替案: 床の既存のタイルに色を乗せて帯を作る(粗いが成立する)。
- 費用の見立て: 要素 1〜6 は既存の仕組みの再利用が中心で、小。要素 7〜9 は T0 の結果次第で省ける。

## 12. 未確認の点と実機で確認すべき点

- レーンの赤橙と Spitter の弾の色・ランタンの光との区別(形で区別する前提)。
- 最も暗い床での 35% のレーンの読み取り(A5 の数値は目標で、実機で確認する)。
- 小さい画面とゲームパッドの操作中に、0.7 s の予告を読んでダッシュまで入力できるか。足りなければ Windup の長さは `game-designer` の判断(`design/combat.md` §7)。見た目の強調では補えない場合は、規則の問題として戻す。
- Recovery の沈んだ見た目の誤読(§7)。
- レーンの幅を接触判定に一致させたことで、プレイヤーが「かすったのに当たらない」「当たったのにかすっただけ」と感じるか。
- 抜けた合図(§9)が過剰な表示にならないか。
- 通常型と突進型の尾根の差が、小さい画面で見分けられるか。
- 技術確認(T0)で、既存のスプライトと演出の仕組みの実際の制約。仕様を満たせない要素があれば、Build から戻る。

## 13. 参照

- `design/combat.md` §10(art への条件)、§2.1、§3、§5。
- D-006(予告の見た目の割り当て)、D-003〜D-005。
- `design/combat.md` §10 からこの文書への参照は、ファイルを書き込めるロールが追記する(Handoff 12 を参照)。
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

<<<FILE sim/build-0.3.md
# Simulated build 0.3 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes
  before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and
  swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step
  aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2
  and minute 15.
- Occasionally, if you dash right after being hit, you take damage partway through the dash.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-002-combat-direction-rooms-and-grub-charge.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-002: 戦闘の単調さへの対応は「部屋の構成と進行」を主軸にし、敵の挙動追加は予告つき Grub 突進の1つに限る

## Decision

G-001 の方向を次のとおり決める。

**主軸: 案2(部屋の構成と進行を作る)**
- 既存の2種類の敵(Grub、Spitter)のまま、部屋ごとに出し方と強さが変わる構成を定義する。
- 時間差で出る波、出現位置の指定、部屋ごとの敵数と数値の段階的な上昇を含む。
- 5部屋の構成で、序盤は基本を覚え、後半は組み合わせの判断が必要になる進行にする。

**併用: 案1のうち「予告つき Grub 突進」の1つだけ**
- Grub に、立ち止まって短く溜めてから直線上に素早く突っ込む型を追加する。既存の Grub の枠組みに挙動を足す形で、新しい敵の種類は作らない。
- 予告は、害を与える前に見えること(柱3)を必須条件にする。予告の長さは秒で定義し、30 FPS と 60 FPS で同じ長さに感じられること。
- 突進を、ダッシュの無敵で抜ける使い道を生む手段として位置づける。

**優先度:** 部屋の構成と進行(案2)が先。Grub の突進は同じ仕様の中で定義するが、実装と検証は案2の構成と合わせて行い、効果を切り分けて見られるようにする。突進を部屋に配置するかどうかは、部屋ごとに外せる形にする。

**この決定が扱わないこと(スコープ外):**
- Spitter の撃ち方の変化、新しい敵の種類は、今回は作らない。案2と突進の結果を見てから、別の判断として扱う。
- 案3のプレイヤー側の数値調整(攻撃回復、被弾後の無敵、ダッシュのクールダウンなど)は、今回は行わない。実機の感触(H1)の確認後に再検討する。
- 案3のキット変更(ダッシュに攻めの使い道を与える、など)は選ばない。ダッシュの役割を変え、柱1の解釈に触れるため、必要になった場合は別途 Owner への Escalation を検討する。今回は不要。
- D-001 の変更、新しい入力ボタン、ラン長(15–20分)、部屋数(5)の変更は行わない。Owner のエスカレーションは不要(トリガーに該当しない)。
- 欠陥 D(被弾直後のダッシュ中のダメージ)は、2b として G-001 に含めるが、この決定の対象外。`qa` の再現結果が出てから、期待される挙動を設計書に書き足す。

## Rationale

- 診断の主因は P1(敵の挙動が単調)と P2(部屋に進行がない)で、設計書と観察が一致している。
- P2 は案2が低コストで戻しやすく、既存システムの再利用という制約に合う。
- P1 を根本から解くのは案1だが、全面的に進めると実装と見た目の作業が大きい。小さなチームの制約を考えると、効果が最も直接的な Grub 突進の1つに絞るのが妥当。突進は C(ダッシュの使い道がない)にも直接効く。
- 案2だけでは数値が上がるだけで「速くなっただけ」になるおそれがある。突進を併用することで、型そのものを変える要素を確保する。
- 案3は、実機の感触が未確認のまま数値を触ることになり、敵が変わらないと不快な縛りに感じられるおそれがある。主案にしない。
- 診断の B3 と C2 は推定にとどまる。確認が取れるまで、プレイヤー側の変更は避ける。

## Alternatives considered

- **案1を全面的に進める(Spitter の変化も含む):** A の根本には最も強く効くが、予告の演出と実装の量が増える。まず小さく試して効果を見る方が、リスクが低い。
- **案2のみ:** 最も安いが、P1 が残り、A の根本が解けない可能性がある。
- **案3を主にする:** 実機の確認がなく、A への効果が小さい。キット変更は柱1の解釈に触れる。
- **Owner にエスカレーションする:** D-001 の枠内で、ビジョンの柱も変えないため、game-director の権限内。

## Revisit when

- 次の Play で、立って振るだけでは後半の部屋で通用しなくなったが、まだ型が単調と感じられる場合(Spitter の変化や敵の追加を検討)。
- 実機の確認で、H1〜H4(操作感、実時間、演出、数値)が単調さの主因だと分かった場合(案3の数値調整を再検討)。
- 突進の予告が柱3を満たせない、または Grub 突進の追加費用が見込みを大きく超えた場合。
- 深みが敵と位置取りだけでは足りないと分かった場合(D-001 の「Revisit when」に該当。その場合は Owner に Escalation する)。
>>>END

<<<FILE decisions/D-003-grub-charge-and-room-rules.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-003: Grub 突進は同時に 1 体・方向固定・予告中は無害とし、部屋は突進スイッチで外せる

## Decision

D-002 の範囲内で、`design/combat.md` に次の規則を置く。数値はすべて暫定値で、H1〜H4 の確認後に調整する。

- Grub 突進は、Windup(0.7 s)で方向を固定してから Charge(8.0 タイル/s、7.0 タイル)に入り、Recovery(0.8 s)で止まる。
- 接触ダメージは Chase と Charge のみ。Windup と Recovery は無害にする。
- 同時に Windup または Charge にある突進型は 1 体まで。
- Windup の長さは全部屋で 0.7 s に揃える。部屋の段階的な上昇は、Grub 速度、Spitter 間隔、敵の数、波、配置で作る。
- 部屋ごとに突進スイッチを持ち、オフのときは突進型を同じスロットの通常型 Grub に置き換える。
- 突進は部屋 2、4、5 に入れる。部屋 1 と 3 には入れない。

## Rationale

- 予告中に害がなければ、予告を「危険の合図」として読める。柱3に合う。
- 同時に予告が複数あると、読む対象が増える。1 体に限れば、他の弾との重なりも読みやすい。
- 方向を固定すると、ダッシュのタイミングの窓(0.25 s)を予告後に作れる。
- Windup を揃えると、突進の効果を、構成の上昇と分けて見られる。
- スイッチは D-002 の「部屋ごとに外せる形」を満たす。

## Alternatives considered

- **予告中も接触ダメージを残す:** 近づく動機は減るが、予告が害を与える前の合図にならない。
- **Windup を部屋ごとに短くする:** 難度は上がるが、読み方が部屋ごとに変わり、柱3の確認が難しくなる。
- **同時に複数の突進を許す:** 圧は上がるが、読めない重なりが生じる。

## Revisit when

- Play で、予告が弾や他の敵と重なると読めないとわかった場合。
- 歩きだけで簡単に避けられ、ダッシュを使う理由が出ない場合。
- 技術確認で、波の出現や状態の追加が既存システムで大きな費用になるとわかった場合。
>>>END

<<<FILE decisions/D-004-technical-approach-grub-charge-and-waves.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-004: 突進と波の技術方針 — 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ

## Decision

`design/combat.md` を実現する技術方針を次のとおり決める。仕様の内容(数値、規則)は変えない。

- **状態の追加**: 突進は共通の敵コントローラに Spawning、Windup、Charge、Recovery を足して実現する。突進型は `grub_charger`(Grub のデータ + 突進の数値)とし、別のコントローラや別クラスは作らない。
- **時間**: 状態のタイマーはゲーム内の経過時間(delta)で進める。delta は 1 更新あたり 0.05 s を上限にする。状態が切り替わるときは余りを次の状態に持ち越す。ポーズ復帰の最初の更新も同じ上限を通す。
- **突進の接触**: Charge 中は、Grub とプレイヤーの相対運動をスイープ判定する(判定形状が円でない場合は相対移動 0.25 タイル以下に分割)。接触の解決は 1 つの関数にまとめ、プレイヤーの無敵は問い合わせ関数を通して読む。無敵の実装自体は変えない。
- **同時 1 体**: 保存する状態は作らない。Windup に入る瞬間に、生きている他の突進型が Windup または Charge にいるかを調べる。
- **突進スイッチ**: スポナーが生成時に `grub_charger` を `grub` に置き換える 1 か所で実現する。
- **部屋データ**: 部屋ごとの数値、スロット、波(スポーン一覧と K/T)を宣言的に持たせる。出現中、最初の 1 発、出現位置の待ちは全部屋共通の定数にする。
- **見た目への口**: 敵の状態、状態の経過割合、突進の方向を、見た目側が読める形で出す。
- **開発用補助**: 部屋選択、スイッチ、30/60 FPS の切り替え、状態ログは開発ビルド限定にする。

仕様と既存実装の食い違い 2 点(Flinch、接触の定義)は、この決定では決めない。計画は仕様の文面どおりに組み、`game-designer` の確認を待つ。

## Rationale

- 共通コントローラは種別ごとの違いをデータと小さなルーチンで持つ構造のため、状態の追加が既存の枠に収まる(小さなチーム、再利用)。
- 突進は 30 FPS で約 0.27 タイル/更新、向かい合うダッシュとの相対で約 0.8 タイル/更新動く。判定形状が仕様にも未定義のため、離散判定は取りこぼしの可能性を排除できない。スイープなら形状の大きさに依存しない。
- 同時 1 体を導出で判定すれば、倒された、部屋が終わった、といった経路での解放漏れが起きない。敵は最大 4 体なので費用も無視できる。
- スイッチをスポナーの 1 か所に置くと、「敵の数、波、位置は同じで突進だけ消える」(V6)が構造で保証される。
- 無敵を問い合わせ関数の裏に置くと、欠陥 D の修正がこの作業と独立する。

## Alternatives considered

- **離散の重なり判定のまま、判定を大きくする**: 形状を変えると仕様の判定の範囲(既存の接触判定)から外れ、窓も変わる。
- **シミュレーション全体を固定時間刻みにする**: 取りこぼしと時間の誤差は消えるが、既存の操作感に触れる範囲が大きく、この Goal の費用を超える。
- **同時 1 体を保存したトークンで管理**: 解放漏れ(Windup 中の撃破、部屋終了、ポーズ)の経路が増える。
- **各コントローラに突進スイッチのフラグを持たせる**: 置き換えの場所が敵ごとに散り、V6 の保証が弱い。
- **突進用に別の敵コントローラを作る**: Chase や Flinch、出現中の処理が二重になる。

## Revisit when

- T0 の調査で、部屋のコードと敵のコントローラが強く結合していた、または部屋の終了条件が広く参照されていた場合(T3 の大きさと並列化を見直す)。
- 接触の判定形状が、スイープまたは分割で扱いにくい形だった場合。
- 欠陥 D の修正が、無敵の問い合わせ関数の前提(1 つの真偽で答える)を変える場合。
- 30 FPS 未満のサポートが必要になった場合(delta の上限を見直す)。
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

<<<FILE decisions/D-006-grub-charge-telegraph-visual.md
---
kind: decision
id: D-006
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-006: 突進の予告は「地面のレーン + 熾火の点灯 + 沈み込み」で示し、赤橙は害になる状態だけに使う

## Decision

`design/grub-charge-telegraph.md` の視覚仕様の基本を、次のとおり決める。後の工程を縛るのは次の割り当て。

- **予告の主な合図**: Windup 中に、Grub の足元から固定した方向へ、地面のレーン(赤橙の半透明の帯、縁取り、突進方向の矢印)を出す。方向は、レーンの向きで示す。幅は既存の接触判定の範囲に一致させ、長さは 7.0 タイルまたは壁の手前までとする。
- **補助の合図**: 体の沈み込み、背中の尾根(熾火)の点灯、目の光。色だけに頼らず、形(レーンと矢印)、動き(沈み込み)、明るさ(点灯とレーンの強さ)を組み合わせる。音は付ける場合の補助であり、音がなくても読めるものとする。
- **色の割り当て**: 脅威の赤橙は、「これから害になる、またはいま害になる」状態(Windup のレーンと点灯、Charge)にだけ使う。出現中は淡い青、Recovery は沈んだ色と蒸気で示し、赤橙は使わない。
- **突進型の目印**: 突進型は、出現時から常に、消灯した暗い赤茶の尾根で通常型と区別する。通常型の見た目は変えない。
- **時間**: すべての見た目の変化は、状態の経過割合から求める。フレーム数に結び付けない。
- **被弾の見せ方**: 突進型への攻撃は、白いフラッシュと火花だけで示す。怯みの動き(のけぞり、位置のずれ、縮み)を予告や状態の表示に使わない。
- **Recovery**: 「止まっていて攻撃が通る」と読ませるために、熾火を消し、沈んだ色と蒸気で示し、最後の 0.2 s で通常の姿勢に戻る。
- **要素の優先度**: 必須はレーン、体の色変調と変形、尾根の重ね絵、被弾フラッシュ、出現中の表示。残像・粒子、傷の重ね絵、接触結果の合図(抜けた合図、使用済み表示)、音は、既存の仕組みで足りない場合に省いてよい。

この決定が扱わないこと: 戦闘の規則と数値(`game-designer`)。色の値は暫定値で、Spitter の弾の色との差などの確認後に値だけを調整してよい(割り当ての方針は変えない)。

## Rationale

- レーンは、方向、通る範囲、時間(明るさの上昇)を 1 つの形で伝える。柱3(害の前に見える)と、「ダッシュで抜けられると判断できる」目標に最も直接効く。
- 幅を接触判定に一致させると、見た目と判定のずれによる「避けたのに当たった」「当たらないのに避けた」を防げる。ダッシュの窓の読みを守る。
- 赤橙を害になる状態に限ると、「赤橙 = 危ない」という美術方針の読みが保たれる。Recovery と出現中を赤橙にしないことで、「無害」を同じ言語で示せる。
- 怯みの動きを使わないのは、D-005 と §10 の条件による。被弾は白いフラッシュに限り、予告の表現と混ざらないようにする。
- 既存の Grub のスプライトに重ね絵と色変調で足すので、新しい大きなアセットが要らない(小さなチームの制約)。

## Alternatives considered

- **体の色の変化だけで予告する**: アセットは最小だが、方向と範囲が分からず、色だけに頼ることになる(§10 の条件に反する)。
- **プレイヤー側の画面端の警告表示(矢印など)**: 画面の小ささと一瞬の判断に向かない。位置と範囲から目が離れる。
- **レーンを判定より少し広く描く**: 読みやすくなるが、窓の読みを狂わせる。採らない。
- **レーンのシェブロンを動かして方向を強調する**: 突進が始まったように誤読される。採らない。
- **Windup の終わりで点滅させる**: 緊迫するが、点滅の回数の制約と FPS 依存の問題がある。明るさの上昇と単発のフラッシュを採る。
- **Recovery を赤橙のままにする**: 害があるように読めて、隙にならない。採らない。
- **Recovery を特別に表示しない**: 隙が読めず、反撃の機会が減る。採らない。
- **突進型を出現中まで通常型と同じ見た目にする**: 部屋 2 を新鮮に学べるが、部屋 4、5 でどの敵が突進するか読めない。尾根の目印を採る。

## Revisit when

- Play で、レーンが暗い床、小さい画面、Spitter の弾との重なりで読めないとわかった場合。
- 実機で 0.7 s の予告が読んでダッシュするのに足りないと感じられ、見た目の強調では補えない場合(規則の問題として `game-designer` に戻す)。
- Recovery の見た目が「死にかけ」「無敵」と誤読される場合。
- T0 の調査で、必須の要素が既存の仕組みで実現できないとわかった場合。
- 別の脅威(新しい敵)を足すことになり、赤橙の割り当てを見直す必要が出た場合。
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

<<<FILE goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 17
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 17: studio → gameplay-engineer — D-004 の方針で Build を再開する(T0 は「前提の台帳」に置き換え)

## Task

`design/combat.md` と `design/grub-charge-telegraph.md` の仕様を、D-004 と D-007 に従って実装する。最初に一括で調査(T0)するのではなく、下の「前提の台帳」の各項目を、それに最初に依存するタスクの冒頭で確認し、前提が崩れたらそのタスクを止めて返す。

## Context

Goal G-001(戦闘の単調さの改善)。D-002 により、主軸は部屋の構成と進行、併用は予告つき Grub 突進の1つ。仕様は `design/combat.md`(D-003、D-005)、突進の予告の見た目は `design/grub-charge-telegraph.md`(D-006)にある。

Build 1 回目(Handoff 13)は、コードやビルド、テスト実行の手段がなく T0 を完了できず、実装なしで `question` を返した。`technical-director` が再検討し、方針(D-004)は保ったまま、T0 を前提の台帳に置き換えた(D-007)。同じ入力で T0 を繰り返しても結果は変わらないので、T0 の再実行や、T0 だけを別担当に任せることはしない。

## Findings

(`technical-director` の計画のうち、実装に必要な客観的内容。)

### 1. 前提の台帳

各項目は「置く前提 / 確認する場所 / 崩れたときの戻し先」。

| # | 項目 | 置く前提 | 確認する場所 | 崩れたとき |
|---|---|---|---|---|
| 1 | 部屋データ、スポナー、波 | 部屋は敵の一覧を最初に全部出す前提かもしれない。波には対応していないと仮定し、スポナーに波の予定(スポーン一覧と K/T)を足す | 部屋のタスクの冒頭。部屋の終了条件がどこから参照されているか | 終了条件が広く参照されている、または敵の生成が部屋のコードと強く結合している → (iii) `technical-director`(D-004 の Revisit 条件) |
| 2 | 部屋のコードと敵のコントローラの分離 | 結合していると仮定する | 部屋のタスクと状態追加のタスクの冒頭。両方が同じファイルや関数を変更するか | 分離が確認できなければ T2 と T3 は直列 |
| 3 | 接触の判定形状、レーン幅の元の値 | 形状は不明として、D-004 のとおりスイープ(円でなければ相対移動 0.25 タイル以下に分割)で扱う。レーン幅は既存の接触判定が使う大きさの 1 つの値から取る | 突進のタスクの冒頭 | スイープ・分割で扱いにくい → (iii)。接触判定の大きさが 1 つに定まらない → (iii)(新しい大きさは決めない。仕様 §3.4 に反する) |
| 4 | Spitter の弾(壁で消える、敵を通り抜ける) | 仕様 §2.1 のとおりに動くと仮定する | 弾の衝突の処理を読んだ時点 | 差が局所的な処理に収まる → (i) 仕様どおりに直す。弾の仕組みを広く変える必要がある → (ii) `game-designer` |
| 5 | 視覚の仕組み(地面層の描画、色変調と変形、重ね絵、HP 表示、被弾フラッシュ、出現演出、粒子、色の近さ) | 使えると仮定しない。必須要素ごとに下の §4 の段階で確認する | 見た目のタスクの冒頭 | §4 のとおり。(iv) |
| 6 | 接触結果の通知 | §3 のとおり D-004 の口に足す | 突進の接触を解決する関数を作る時点 | §3 のとおり |
| 7 | 敵の挙動が経過時間で進むか | 可変 delta の記述から時間ベースと仮定する | 状態追加のタスクの冒頭。状態遷移や攻撃の間隔がフレーム数で進んでいないか | 触るコードの範囲でフレーム数を使う箇所があれば (i) delta に直す。触らない範囲で見つけた場合は記録するだけで直さない(スコープ外) |

分類 (i)〜(iv) の詳細は D-007 の 2 に従う。(i) はその場で仕様どおりに直す、(ii) は `game-designer`、(iii) は `technical-director`、(iv) は `art-director` への戻し(いずれも Studio 経由)。

### 2. 崩れたときの共通手順

1. 崩れたタスクを止める。他の独立したタスクは続けてよい。
2. 台帳の番号、観察した事実、影響する範囲を書く。
3. D-007 の 2 の (i)〜(iv) のどれかに分類し、(i) 以外は返す。
4. 推測のコードは 1 か所の継ぎ目の後ろに置く。

### 3. 接触結果の通知(台帳 6)

視覚仕様の要素 9 は D-004 の「見た目への口」に含まれていなかったため、追加する(D-007 の 6)。接触を解決する関数(D-004 のとおり 1 つにまとめる)は、結果(未解決 / 抜けた / 被弾)をすでに持つ。その値を、その突進の間だけ保持する値として見た目側から読めるようにし、突進の開始時に未解決へ戻す。費用は小。優先度は S で、継ぎ目が不自然に大きくなる場合は省いてよい。省いたときは、視覚仕様 §6 の使用済み表示と §9 の抜けた合図を省く(D-006 が許している。必須の予告は成立する)。省いた場合は報告に書く。この追加は仕様を変えない。

### 4. 視覚要素の確認の段階(台帳 5)

- 要素 1(状態、経過割合、方向)は自分で作る口で、既存の仕組みに依存しない。
- 要素 2〜6 は既存の描画の仕組みに依存する。確認できなかった場合の段階:
  1. 要素 3(変形)がない → 視覚仕様 §11 の縮小案(変形なし。尾根と目の点灯とレーンで予告)。
  2. 要素 4(重ね描き)がない → 体の縁の色変調で代用(§11)。
  3. 要素 2(レーン)が地面層の矩形としてできない → 床のタイルに色を乗せる代替案(§11)。
  4. どの方法でもレーンの向きと範囲が出せない → 縮小では済まない。作業を止めて返す(iv、`art-director` へ)。
- 縮小案を使った場合は、報告に使った段階を必ず書く(受け入れ基準の読み替えは `art-director` が判断する。ここで受け入れ基準を変えない)。
- 要素 7〜10 は、既存の仕組みで足りない場合は省く。

### 5. 並列化

既定は直列。T2(敵の状態追加)と T3(部屋・波)を並列にするのは、台帳の項目 2 で両者が同じファイルや同じ関数を変更しないと確認できたときだけ。並列にする場合は、分けた作業場所で行う。見た目のタスクは、状態・経過割合・方向・接触結果の口が決まってから始める。口の形が固まれば T2 と並行できるが、既定は直列。

### 6. 無敵の問い合わせ関数と無敵タイマー

- 突進の接触の解決が使う無敵の問い合わせ関数は、現在のフラグを読んで 1 つの真偽で答える設計のまま。署名は変えない。
- 無敵のタイマーのコードには触れない(欠陥 D は今回の範囲外で、`qa` の再現は別ステップで進行中)。`sim/repo-notes.md` には、無敵フラグを 2 つのタイマーが共有していると書かれている。
- `design/combat.md` の V3、V4 の測定は、仕様どおり、直前 0.8 s 以内に被弾していない状態で行う前提。

### 7. テスト戦略

既存のテストの有無と枠組みは不明。
- 枠組みがあれば、固定 delta での決定的なテスト(状態の長さ、接触の 1 回の解決、同時 1 体、スイッチ)を足す。
- 無ければ、開発ビルド限定の状態ログと 30/60 FPS の切り替え(D-004)を作る。`qa` が `design/combat.md` の V1〜V11 で確認する。

### 8. 打ち切りの条件(D-007 の 7)

読める・書けるコードが全くない場合は、再試行せずに `outcome: question` で返す。Build 1 回目の報告は「T0 を実施できなかった」であり、「コードを書けない」とは報告されていない。今回、実際にコードを読み書きできるかどうかを最初に報告すること。

## Decisions already made

- D-001: ワンボタン戦闘。新しい入力ボタンなし。
- D-002: 主軸は部屋の構成と進行。併用は予告つき Grub 突進の 1 つのみ。
- D-003: 突進は同時に 1 体・方向固定・予告中は無害。部屋は突進スイッチで外せる。
- D-004: 技術方針(共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ)。
- D-005: 突進型は 3 状態で怯まない。接触は突進ごとに最初の重なりで 1 回だけ解決。「遠い方」は出現を決める時点で選ぶ。
- D-006: 突進の予告の見た目(地面のレーン + 熾火の点灯 + 沈み込み)。赤橙は害になる状態だけに使う。
- D-007: T0 を前提の台帳に置き換える。崩れたときの戻し先、推測の封じ込め、接触結果の通知の追加、打ち切りの条件。

## Constraints

- 戦闘の規則・数値・仕様、D-001〜D-006 は変えない。
- 新しい入力ボタンなし。開発用補助(部屋の選択、突進スイッチ、30/60 FPS 切り替え、状態の遷移ログ)は開発ビルド限定で、プレイヤー向けの新しい入力は足さない。
- 30 FPS と 60 FPS の両方で正しく動くこと(D-004 の delta 上限 0.05 s、状態切り替え時の余りの持ち越し)。
- 小さなチーム: 既存の仕組みを再利用する変更を優先する。
- 無敵のタイマーのコードには触れない。
- 実行できなかった確認を「通った」と書かない。
- 仕様が曖昧・矛盾・欠落している場合は自分で決めず、返す(Studio が `game-designer` に回す)。

## Open questions

None。

## Expected output

1. 実装(変更・テストまたは開発ビルド限定の状態ログ・ビルドの手順)と、ビルドノート。
2. 報告は次を分けて書く: 確認できたこと、確認できなかったこと、その理由。台帳 1〜7 のそれぞれについて、確認した結果(前提どおり / 崩れた / 未確認)と、使った分類 (i)〜(iv) を書く。視覚要素は使った段階(§4)を書く。接触結果の通知を省いた場合は、それも書く。
3. 前提が崩れて止めた場合は、§2 の手順で書き、`outcome: question` で `studio` に返す(Studio が D-007 の分類に従って `technical-director` / `game-designer` / `art-director` に回す)。コードを読み書きできない場合は §8 に従い、再試行せず `outcome: question`。
4. 出力の宛先は `to: studio`(Verify で `qa` と `art-director` を並列にするため、Studio が受け手ごとに Handoff を組み直す)。`## Sender assessment` に自己確認の評価を書いてよいが、`qa` には渡されない。
5. 実装が完了した場合は `outcome: done`。ゲームの検証の判定(合否)は `qa` が行うので、自分で合格と宣言しない。

## Sender assessment

Studio の process 上の見立て(ゲームの内容の判断ではない): Handoff 16 の Sender assessment は転記していない。Handoff 16 の Findings のうち、実装に必要な客観的内容のみを抜き出した。`technical-director` が残していたリスクは、Build が書き換えられるコード自体がない場合に計画が空になること。そのため、最初にコードを読み書きできるかの報告を求めた。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, sim/repo-notes.md, sim/build-0.3.md, design/combat.md, design/grub-charge-telegraph.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-005-flinch-contact-and-far-slot-rules.md, decisions/D-006-grub-charge-telegraph-visual.md, decisions/D-007-build-without-code-access-assumption-register.md
- Previous handoff: none(Handoff 16 に Sender assessment があるため渡さない。計画の内容は上の Findings と D-007 に含めた)
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
