# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/31-studio-to-gameplay-engineer.md
next_seq: 32

## You may write

- goals/G-001-combat-monotony/32-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/31-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 31
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 31: studio → gameplay-engineer — 変更内容の修正(F-1)と、V7・V10 で確認できなかった点の明記

## Task

模擬ビルド 0.4 の検証(Handoff 30)で見つかった仕様との食い違い F-1 を、変更内容の記述(Handoff 28 の 2.1〜2.4)で仕様に合わせて直す。あわせて、QA が記述から確認できなかった V7(Grub の速度、遠い角が同距離のときの規則)と V10(プレイヤー側の数値)を、変更内容に明記して確定する。

## Context

G-001 は戦闘の単調さの改善。D-008 により、Build は変更内容を Handoff に正確に書いた時点で完了で、模擬ビルド(`sim/build-0.4.md`)はその記述からシミュレーターが作る。Verify(Handoff 30)では V1〜V12 のうち fail はなかったが、V7 と V10 の一部は記述から確認できず pass にできなかった。基準の外で、仕様と模擬ビルドの食い違い(F-1)が 1 件あった。すべて模擬ビルドの記述に基づく結果で、実機の観測ではない。

## Findings

Handoff 30(`qa` の報告)から、客観的な事実だけを抜き出す。

1. **F-1(仕様との食い違い)**: 突進の再開始の待ち時間の起点が違う。
   - 仕様 `design/combat.md` §3.3: 前回の **Recovery が終わってから** 2.5 s 以上。
   - 模擬ビルド: 前回の**突進が終わってから** 2.5 s 以上(Recovery 0.8 s を含む)。
   - 影響: 同じ Grub の次の突進の条件が仕様より 0.8 s 早くそろい、突進の頻度が上がる。V1、V5、§3.5 は壊れない。
2. **V7 の未確認 1: Grub の速度**。仕様は部屋 1〜5 で 2.0 / 2.0 / 2.2 / 2.2 / 2.4。模擬ビルドは部屋 3 を「部屋 1〜2 より少し速い」、部屋 5 を「最も速い」としか書いておらず、部屋 4 に言及がなく、数値がない。
3. **V7 の未確認 2: 「遠い角」が同距離のとき**。FL を選ぶ規則と、距離を中心間で比べることが、模擬ビルドの記述にない。
4. **V10 の未確認**: 模擬ビルドの記述にあるプレイヤー側の数値はダッシュの 0.25 s の保護だけで、仕様と整合する。攻撃の回復 0.35 s、ダッシュのクールダウン 0.6 s、被弾の硬直 0.3 s と無敵 0.8 s は、変更した・していないのどちらの記述もない。
5. **補足(確認のみ。修正を求めない)**: V12(c) について、同じ波の複数スロットの待ちが「波を出すと決めた時点から同時に始まる」ことが模擬ビルドに明記されていない(「スロットごとに別々」とだけある)。基準の結果には影響しない。記述に 1 文あると確認しやすい。
6. **範囲外(触らない)**: 欠陥 D(被弾直後のダッシュ中にダメージを受けることがある)。模擬ビルドはこの挙動を記述しており、仕様は意図的に未定義。規則は `game-designer` が決める事項で、この Step では変更も原因の推測もしない。

## Decisions already made

- D-001: 攻撃とダッシュのみ。新ボタンなし。
- D-004: 技術方針(共通コントローラへの状態追加など)。
- D-005: 怯み、接触の解決、「遠い方」は出現を決める時点で選ぶ。
- D-007: 前提の台帳。確認できない項目は「模擬上の前提」と明記する。
- D-008: Build は変更内容を正確に書いた時点で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- 仕様は `design/combat.md` が正。食い違いは仕様に合わせて変更内容側を直す。
- 仕様に数値や規則がなく、決められない場合は決めずに返す(Skill どおり)。その場合は、仕様のどの節が欠けているかを書く。
- 実コードで確認済みと書かない。確認できない項目は「模擬上の前提」と明記する。
- 新しい入力ボタンを足さない。プレイヤー側の数値を変えない。
- 欠陥 D の原因を推測して書かない。

## Open questions

1. F-1 は、仕様 §3.3 の文面どおり「Recovery が終わってから」でよいか。仕様の文面が曖昧と判断する場合は、直さずに `game-designer` への質問として返す。
2. 遠い角が同距離のときの選び方は、仕様または D-005 に定義があるか。ある場合はそれを変更内容に明記する。ない場合は決めずに返す。
3. Grub の速度(部屋 1〜5)は、仕様の数値をそのまま変更内容に書いてよいか。変更内容にすでに数値があるなら、模擬ビルドで落ちた理由は分からないので、そのとおり報告する。

## Expected output

- Handoff を `to: studio` で書く(Verify で `qa` に渡す Handoff を Studio が組み直すため)。
- Findings に、**修正後の変更内容 2.1〜2.4 の全体**を自己完結で書く(Handoff 28 を読まなくても分かる形)。次を含める。
  - F-1 の修正(起点を Recovery 終了後にする)。
  - 部屋 1〜5 の Grub 速度の数値。
  - 遠い角が同距離のときの規則と、距離の比べ方(仕様に定義がある場合)。
  - プレイヤー側の数値(攻撃の回復、ダッシュの保護とクールダウン、被弾の硬直と無敵)を変更していないという明記。
  - 追加の 1 文: 同じ波の複数スロットの待ちは、波を出すと決めた時点から同時に始まる(仕様 §4.1、D-009 と矛盾しない場合のみ)。
- 変更した箇所を、Handoff 28 との差分として一覧する。
- 模擬上の前提が残る項目を一覧する。
- 自己評価は Sender assessment にだけ書く。
- 仕様の欠落や矛盾があれば、決めずに `outcome: question` で返す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md、sim/build-0.4.md、goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md(修正する変更内容の元。自分で書いたもの)
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/30-qa-to-studio.md
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
# Simulated repository notes — lantern-depths (build 0.4)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a Playtester.

Facts carried over from build 0.3 and still true:
- Enemies share one controller. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: a hit enemy enters a 0.2 s Flinch that interrupts anything, including Attack, then returns to Chase. Not described in `design/combat.md`.
- The player's attack is a short arc hitbox. Enemies take damage on overlap. No blocking or facing.
- Player invulnerability is one on/off flag. The dash sets it and starts a 0.25 s timer. Getting hit sets it and starts a timer ending 0.8 s after the hit. Each timer clears the flag when it ends, so a dash within 0.8 s of a hit loses protection mid-dash. This code was not touched.
- Movement is simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- The game loop uses variable delta; 30 and 60 FPS are supported.

Changes (described, not built or run; assumptions from the register are unverified against real code):
- Delta is capped at 0.05 s per update, including the first update after unpausing. State timers use delta, carry leftovers into the next state, and stop while paused.
- Room data now holds waves (spawn list of type and slot), next-wave condition (K, T), Grub speed, Spitter interval and charge switch. Spawn timings (fade-in 0.8 s, first Spitter shot 1.0 s after fade-in, spawn wait at 4 tiles up to 2.0 s) are shared constants. Six slots: Door, Far, L, R, FL, FR, with coordinates in room data. Assumed previously: room data held an enemy list, slot coordinates and an end condition, and everything spawned at once.
- Spawner: wave 1 at room start. Wave N+1 spawns when living enemies ≤ K or T seconds after the last enemy of wave N finished fading in (after any wait), whichever is first. Living enemies include fading-in enemies and exclude those waiting at a slot. K and T are checked only once every enemy in wave N has started fading in. This start point is logged and set in one place. For waves without waiting enemies it is the spawn decision.
- Slot waiting: per slot, checked from the spawn decision, player-to-slot center distance under 4 tiles waits up to 2.0 s. A slot that finished waiting does not wait again. The player is not pushed out of a slot.
- Far corner choice (FL or FR): the farther one from the player at the spawn decision, FL on ties, fixed during the wait.
- Charge switch: one place in the spawner replaces `grub_charger` with `grub` when off. No visuals are added in that case.
- Spawning state for all enemies: 0.8 s, no movement, no action, no damage to the player, no damage or flinch from the player. Then Chase.
- Spitter projectile: 4.0 tiles/s, 1 heart, straight to the player's position at the moment of firing, vanishes on walls, passes through enemies. Flinch unchanged.
- `grub_charger`: Grub data (HP 2, room Grub speed) plus charge numbers, in the same controller, with states Spawning, Chase, Windup 0.7 s, Charge, Recovery 0.8 s. Charge goes at 8.0 tiles/s in a direction fixed at wind-up start, to 7.0 tiles or a wall, and leftover distance converts to time carried into Recovery. Entry to Windup: ≥1.5 s since Spawning ended, ≥2.5 s since last Recovery ended (flinch does not reset), distance 3.0–6.0, and no other living `grub_charger` in Windup or Charge (derived by scanning enemies, no stored token). Update order for simultaneous eligibility is the existing enemy order.
- Contact resolution during Charge only, in one function: per-update swept overlap, first overlap per charge is the contact; already overlapping at charge start counts on the first Charge update. The invulnerability query reads the flag as seen this update. Invulnerable gives "slipped through" (no damage), otherwise the existing damage routine applies 1 heart once and the result is "hit". The result stays for the rest of the charge. It resets to unresolved at Windup and Charge start. The visuals read it.
- Damage routine change: Spawning enemies ignore hits. A `grub_charger` in Windup, Charge or Recovery loses HP only, with no Flinch, knockback or state/direction/timer change. All other cases flinch 0.2 s. HP 0 kills immediately in any state.
- Visuals (stage 0 art, no reduced fallback): fade-in with a blue ring; ember ridge overlay on charge-type Grubs only; floor lane drawn below characters and projectiles, self-lit, clipped to 7 tiles or the wall using the charge collision test, width from the enemy contact width value; body squash/stretch is render-only; afterimages every 0.5 tiles; one new particle type (afterimage, dust, steam, sparks); white hit flash 0.1 s; crack overlay at HP 1; pale ring at the player for 0.15 s on "slipped through". No audio.
- Dev build only: room select 1–5, per-room charge switch, 30/60 FPS toggle, and a state transition log (including the wave all-fading-in moment). No new player inputs.

Open assumptions (unconfirmed): contact shape and size of enemies; slot coordinates; whether other enemy timers (bite interval) use delta; room end condition coupling to wave spawning; lane/projectile/lantern color similarity.
>>>END

<<<FILE sim/build-0.4.md
# Simulated build 0.4 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. Lengths are in seconds, distances in tiles. Everything below holds the same at 30 FPS and 60 FPS unless a difference is stated.

## Rooms and waves

- Every room now sends its enemies in two waves. The first wave appears when the room starts. The second wave appears when the number of living enemies drops to the room's threshold, or when the timer runs out, whichever happens first.
- Enemies that are fading in count as living. Enemies still waiting to appear do not count.
- Room 1: wave 1 is two ordinary Grubs, left and right. Wave 2 is one ordinary Grub at the far side. It comes when one or fewer Grubs are alive, or 10 s after the last wave-1 Grub finished fading in. 3 enemies in total, at most 2 at once.
- Room 2: wave 1 is one charging Grub at the far side. Wave 2 is two ordinary Grubs (left, right) and one more charging Grub (far). It comes when the wave-1 Grub is dead, or 15 s after it finished fading in. 4 enemies in total, at most 3 at once.
- Room 3: wave 1 is a Spitter at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in whichever far corner is farther from you at the moment the wave is triggered, and an ordinary Grub on the right. It comes at one or fewer alive, or 12 s. 4 enemies in total, at most 3 at once. Spitters fire every 2.0 s, and Grubs move slightly faster than in rooms 1–2.
- Room 4: wave 1 is a Spitter in the far-left corner, a charging Grub at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in the far-right corner and a charging Grub on the right. It comes at one or fewer alive, or 12 s. 5 enemies in total, at most 3 at once. Spitters fire every 1.8 s.
- Room 5: wave 1 is a Spitter at the far side and two ordinary Grubs, left and right. Wave 2 is a Spitter in the farther far corner and two charging Grubs, left and right. It comes at one or fewer alive, or 12 s. 6 enemies in total, at most 4 at once. Spitters fire every 1.6 s, and Grubs are the fastest here.
- A room ends when every wave has appeared and every enemy is dead.
- The spot a farther-corner Spitter picks is decided when the wave is triggered. If you move while the wave waits, it does not change.

### Standing near a spawn point

- If you are closer than 4 tiles to the spot where an enemy would appear, that enemy does not appear yet. It appears as soon as you are 4 tiles or farther away, or after 2.0 s of waiting, whichever comes first. Each spot waits on its own. A spot that has finished waiting does not wait again if you walk back to it. You are not pushed away from a spot, and the enemy can appear on top of you.
- While some enemies of a wave are still waiting, the next wave's threshold and timer are not running. They start counting only once every enemy in the wave has begun fading in.
  - Room 1: stand near the left spot only. The right Grub appears, and the second wave does not come while the left spot waits. If you kill the right Grub during the wait, the moment the left Grub begins fading in only one enemy is alive, so the Grub from wave 2 comes immediately. If you did not kill it, two are alive, and the second wave comes after one is killed or 10 s after the later one finished fading in.
  - Room 2: the charging Grub waiting at the far side blocks the second wave entirely until it starts fading in. After that, the second wave comes when it is dead, or 15 s after it finished fading in. It cannot be hit during the first 0.8 s of fading in, so the earliest kill is after that.
  - Waves with no waiting spots start counting the moment they appear.

## Enemies appearing

- Every enemy fades in for 0.8 s: from 40% to full opacity, with a pale blue ring at its feet. During this time it does not move, does not attack, does not hurt you, and your swipes do nothing to it (no damage, no flinch).
- A Spitter fires its first shot 1.0 s after it finishes fading in, then at the room's interval. A Spitter shot travels at 4 tiles/s straight at where you stood when it fired, costs 1 heart, vanishes on walls, and passes through enemies without hurting them. Spitters flinch for 0.2 s when hit, as before.

## Charging Grubs

Charging Grubs (rooms 2, 4, 5) look like ordinary Grubs with a dark ember-colored ridge on the back, visible from the moment they fade in. Ordinary Grubs have no ridge. They have 2 HP and walk and bite like ordinary Grubs. In Chase they flinch for 0.2 s when hit.

A charging Grub starts a charge only when all of the following hold:
- at least 1.5 s have passed since it finished fading in, and at least 2.5 s since its last charge ended;
- you are 3.0 to 6.0 tiles away;
- no other living charging Grub is currently winding up or charging.

Flinching does not reset these waits. If two charging Grubs qualify in the same moment (room 5, wave 2, left and right), one of them goes first, and which one is not predictable. The other waits until the first has finished charging.

The sequence:
1. **Wind-up, 0.7 s.** The Grub stops where it stands and its walking animation stops. A red-orange lane appears on the floor from the Grub toward where you were when the wind-up began. The lane is as long as the charge will be, 7 tiles or less if a wall is in the way, and about as wide as the Grub's body. It has a bright edge, a dark underline and a chevron every tile pointing along the lane, and it stays lit regardless of floor darkness. Spitter shots, fading-in enemies and other enemies are drawn on top of it. The lane fades from 35% to full brightness over the wind-up. The Grub squashes to 80% height, widens a little and leans back from the lane. The ridge and eyes warm from dark to red-orange, turning pale-yellow in the final 0.1 s. The direction is fixed; moving afterwards does not turn the lane. The Grub does no damage during the wind-up.
2. **Charge.** The Grub rushes along the lane at 8 tiles/s for up to 7 tiles, or until it hits a wall, and stretches long and thin with a bright core and red-orange edge. The lane flashes extra bright once at the start, stays at full brightness, and disappears behind the Grub as it passes. The part in front stays until the charge ends, then everything fades out over 0.1 s. Afterimages appear every half tile and fade over 0.2 s, with dust at its feet. It passes through other enemies without hurting them. Charge time is about 0.9 s for a full-length run.
3. **Recovery, 0.8 s.** The Grub stands still, sunk to 90% height and tinted a dull grey-blue, with thin steam rising from its feet every 0.3 s. Ridge and eyes go dark. It returns to normal in the last 0.2 s and goes back to chasing.

### Getting hit by a charge

- A charge can hurt you at most once. The first time the Grub's body overlaps you during a charge decides it. If it was already overlapping you as the charge began, that counts as the first moment.
  - If you are invulnerable at that moment (for example, mid-dash), you take nothing. A thin pale white-blue ring appears around you for 0.15 s, and the Grub keeps running through you. The Grub's core dims to a darker red-orange for the rest of the charge. Staying inside it afterward, or the dash ending while it still overlaps you, does not hurt you.
  - If you are not invulnerable, you lose 1 heart, with the normal hit reaction and the normal invulnerability afterward. The core dims in the same way. No ring appears.
- Overlap during the wind-up or recovery does nothing. A new charge starts the count again.
- The invulnerability check reads the state shown at that frame. At 30 FPS the edge of the dash's 0.25 s protection can differ from 60 FPS by up to one frame (about 0.034 s).

### Hitting a charging Grub

- During the wind-up, charge and recovery, your swipes lower its HP only. It does not flinch, is not pushed back, and does not change direction, speed or timing. It flashes white for 0.1 s with small sparks at the point of impact. The lane and ridge do not change.
- With 1 HP left, a small crack mark appears on its body.
- At 0 HP it dies immediately in any state. A dying winder or charger removes its lane within 0.1 s, and another charging Grub may then start its own wind-up.
- Charging Grubs, ordinary Grubs and Spitters not in these three states flinch 0.2 s as before.

## Timing at 30 and 60 FPS

- Fade-in, wind-up, charge distance, recovery, wave timers and waiting are all counted in real time. Durations at 30 FPS are within about 0.034 s of those at 60 FPS.
- Whether a charge touches you does not depend on the frame rate.
- Pausing freezes all timers and animations, including lanes, steam and rings. Resuming after a long pause does not skip ahead more than a short step.
- Nothing flashes more than three times per second, apart from single flashes.

## What play feels like now

- Rooms 1 and 3 behave like before but with two waves, so there is a second arrival to deal with.
- In rooms 2, 4 and 5, standing still in a corner and swiping no longer works: a lane appears, and about 0.7 s later a Grub runs the length of it. Moving off the lane or dashing through the Grub avoids damage. Swiping the Grub during the run only chips it and does not stop it.
- Only one charging Grub is ever winding up or charging at a time.
- No new sounds. No new buttons.
- As before, occasionally, if you dash right after being hit, you take damage partway through the dash. This also applies to a charge that reaches you at that moment.

## Development build only

- A tester can pick room 1–5, switch charging Grubs on or off per room (off turns every charging Grub into an ordinary Grub, with no ridge and no charge), and switch between 30 and 60 FPS.
- A log lists state changes with game time, enemy and type, charge direction, contact result (unresolved, slipped through, hit), wave arrivals with spots, which corner was chosen, the distance to you when a wind-up began, and the moment all enemies of a wave have begun fading in.
>>>END

<<<FILE goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 28
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 28: gameplay-engineer → studio — Build の変更内容の記述を確定した(Handoff 22 の 2.1〜2.4 に D-009 を統合。自己完結)

## Task

Handoff 22 の変更内容の記述(2.1〜2.4)に D-009 の規則を 2.1 の 1 文として足し、確定した全体を、Handoff 22 を読まなくても分かる形で書く。あわせて、模擬上の前提が残る台帳の項目を Handoff 17 の番号で挙げる。

## Context

G-001(戦闘の単調さ)。D-008 により、Build は変更内容を正確に書いた時点で完了する。実コードの変更、ビルド、テスト、動作確認は行っていない。以後の Verify・Play・Review は、この記述からシミュレーターが作る模擬ビルドに基づく。

Handoff 22 は、波 2 以降の条件を調べ始める時点が仕様にないとして `question` で返した。これは D-009(`design/combat.md` §4.1、V7、V12)で決定済みである。今回は 2.1 のスポナーの動きに D-009 の 1 文を足し、Handoff 22 の他の内容は変えていない。

Handoff 22 と D-009 の食い違いの確認結果は、Open questions に書く。

## Findings

### A. 確定した変更内容

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

合計は 部屋 1: 3 体、2: 4 体、3: 4 体、4: 5 体、5: 6 体。同時に存在する敵の最大は 部屋 1: 2、2: 3、3: 3、4: 3、5: 4。部屋は、全部の波が出現し、全部の敵が倒れたときに終わる(既存の終了条件はそのまま使う)。

**スポナーの動き**:
- 波 1 は部屋の開始時に出す(各スロットの出現位置の待ちは次項)。
- 波 2 以降は、「生きている敵が K 体以下」または「前の波の最後の敵の出現中が終わってから T s」の先に起きた方で出す。「生きている敵」には出現中の敵を含める。T の起点は、その波の最後の敵の出現中が終わった時点(出現位置の待ちがあれば、待ちが終わって出現中も終わった時点)である。
- **波の条件を調べ始める時点(D-009。今回足した 1 文)**: 波 N の次の波(N+1)の K と T は、波 N の全員が出現中に入った時点から調べ始める。それより前は、K の判定も T の計測もしない。そのため、出現位置の待ちに入っている敵は「生きている敵」に数えず、出現中に入った時点から数える。
  - 全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波を出す。そうでなければ、K 体以下になるか T s たつかの先に起きた方で出す。T の起点は上のとおりで変わらない。
  - 待ちの敵がいない波では、出現を決めた時点が、そのまま調べ始める時点になる(従来どおり)。
- **出現位置の待ち**: スロットごとに、出現の時点でプレイヤーとスロット座標の距離(中心間)が 4 タイル未満なら待つ。距離が 4 タイル以上になるか、待ちが 2.0 s に達したら、そのスロットの敵が出現中に入る。待ちはスロットごとに別々で、同じ波の待ちは、波の出現を決めた時点から同時に始まる。いったん待ちが終わったスロットは、プレイヤーが戻ってきても待ち直さない(`design/combat.md` §4.1 の既存の文面。追加の規則ではない)。プレイヤーがスロットに重なっていても押し出さない。
- **「FL / FR のうち遠い方」**: その波の出現を決める時点(待ちを始める前)のプレイヤー位置から FL と FR の座標への距離を比べ、遠い方を選ぶ。同じ距離なら FL。待ちの間にプレイヤーが動いても選び直さない。同じ波で FL か FR が別の敵に固定されている場合は、この規則の対象外。
- **突進スイッチ**: スポナーが敵を生成する 1 か所で、スイッチがオフなら `grub_charger` を `grub`(通常型)に置き換える。敵の数、波、スロット、K/T は変わらない。スイッチがオフでも、尾根の重ね絵など突進の見た目は何も付かない。部屋 1、3 には突進型がいないので、スイッチは効かない。

#### 2.2 敵コントローラ(共通)

**出現中(Spawning)**: 全種類の敵に追加する。長さ 0.8 s。この間は、動かない、行動しない、ダメージを与えない、プレイヤーの攻撃のダメージも怯みも受けない。終わると通常の状態(Chase)に入る。Spitter の最初の 1 発は出現中の終了から 1.0 s 後。以降は部屋ごとの間隔。

**Spitter の弾**: 速度 4.0 タイル/s、ダメージ 1 ハート。撃った瞬間のプレイヤーの位置へ直進(先読みなし)。壁で消え、敵の体を通り抜けて敵にダメージを与えない。弾の仕組みは作り直さない。Spitter 自身の怯みは既存のまま(0.2 s)。

**`grub_charger`(突進型)**: Grub のデータ(HP 2、速度は部屋の Grub 速度)に突進の数値を足したもの。別のコントローラは作らない。状態は Spawning、Chase(既存)、Windup、Charge、Recovery。通常型 Grub と同じ Chase、噛みつき、怯みの既存のルーチンを使う。

| 状態 | 長さ | 動き | 接触ダメージ | 怯み・ノックバック |
|---|---|---|---|---|
| Chase | 条件まで | 既存どおりに歩く | あり(既存の噛みつき、1 ハート) | 既存(0.2 s) |
| Windup | 0.7 s | その場で停止、歩行アニメーションも止める | なし | なし |
| Charge | 7.0 タイル進むか壁まで | 固定した方向へ 8.0 タイル/s で直進 | 突進ごとに 1 回まで(下記) | なし |
| Recovery | 0.8 s | その場で停止 | なし | なし |

**Chase → Windup の条件**(Chase の各更新で調べる。すべて満たすとき):
1. 出現中が終わってから 1.5 s 以上たっている。前回の Recovery が終わってから 2.5 s 以上たっている(まだ Recovery がなければ後者は満たすとみなす)。
2. プレイヤーとの距離(中心間)が 3.0〜6.0 タイル。
3. この Grub が `grub_charger` である(スイッチがオフなら生成されない)。
4. 生きている他の `grub_charger` が Windup または Charge にいない。Windup に入る瞬間に、生きている敵を調べて導く。保存する状態(トークン)は作らない。

Chase 中の怯みでこれらのタイマーは巻き戻さない(起点は出現中の終了と前回の Recovery の終了で、怯みは影響しない)。

**Windup**: 入る瞬間のプレイヤーの中心へ向かう単位ベクトルを突進方向として固定する(距離が 3.0 タイル以上なので零ベクトルにならない)。その後プレイヤーが動いても変えない。0.7 s たつと Charge に入る(余りは持ち越す)。

**Charge**: 毎更新 8.0 × delta の距離を固定方向へ進む。通算 7.0 タイルに達するか、既存の移動処理が壁で止めたら終わり、すぐ Recovery に入る(壁に当たったときの特別な処理はない)。7.0 タイルを超えた分は、時間に直して(超過距離 ÷ 8.0)Recovery の経過時間に持ち越す。他の敵の体は通り抜け、ダメージを与えない。

**Recovery**: 0.8 s たつと Chase に戻る。

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

### B. 受け入れ基準 V7、V12 の追跡(記述の上でのみ。満たしたとは書かない)

- V12(a) 部屋 2: Far の突進型が待つ間は、全員が出現中に入っていないので、K=0 の判定も T の計測も始まらない。波 2 は出ない。出現中に入った時点で調べが始まり、生きている敵は 1 体で K=0 より多い。突進型を倒す(出現中の 0.8 s はダメージを受けないので、倒せるのは出現中が終わってから)か、その出現中の終わりから 15 s たつかの先に起きた方で、波 2 が出る。
- V12(b) 部屋 1: L だけ待つ場合、R の Grub は先に出現中に入る。L が出現中に入るまで調べは始まらない。入った時点で 2 体(倒していない場合)なら K=1 より多く、1 体倒すか、最後の敵の出現中の終わりから 10 s たつかの先に起きた方で、波 2 が出る。**待ちの間に R の Grub を倒していた場合は、L が出現中に入った時点で生きている敵が 1 体(K=1 以下)になり、波 2 がすぐ出る。** Verify はこの場合の期待値を「すぐ出る」と読む。
- V12(c): 待ちの間にプレイヤーが 4 タイル以上離れると、その時点で敵が出現中に入る。同じ波で複数のスロットが待つ場合は、全員が出現中に入るまで調べは始まらない。
- V12(d): 待ちのない波は、出現を決めた時点が調べ始める時点。従来どおり。
- V7: 「生きている敵」(出現中を含み、待ちの敵を含まない)、T の起点(最後の敵の出現中の終わり)、調べ始める時点が、2.1 と矛盾しない。「遠い方」の選択は出現を決める時点で固定し、この規則は触れない。

### C. 他の受け入れ基準との対応(どの変更で満たす想定か)

V1〜V6、V8〜V11、A1〜A13 の対応は Handoff 22 の対応表のとおりで、変更はない。要点: 予告は Windup の完了後にしか Charge に入れない(V1)。接触は最初の重なり 1 回(V3、V4)。同時 1 体は導出(V5)。スイッチはスポナーの 1 か所(V6)。怯みは 2.2 の「ダメージを受けたとき」(V11)。レーンの幅、向き、不透明度は 2.3(A1〜A4)。未確認の A5(暗い床での明るさの比)と A10(5 つの見た目の区別)は、模擬ビルドで確かめる。

### D. 模擬上の前提が残る台帳の項目(Handoff 17 の項目番号)

凡例: **模擬上の前提** = `sim/repo-notes.md` が答えず、前提として置いたもの。実コードで確認済みではない。`sim/repo-notes.md` にはスポナー、部屋、波、出現位置、出現中の記述がない。

| # | 項目 | 結果 | 前提の内容 |
|---|---|---|---|
| 1 | 部屋データ、スポナー、波 | 模擬上の前提 | 部屋データは敵の一覧、スロット座標、終了条件を持つ。波はなく最初に全部出す作りで、スポナーに波の予定(スポーン一覧と K/T)を足せる。終了条件は広く参照されていない。D-009 の規則も、この前提の中で持つ。具体的には、(a) 敵の一覧で「生きている敵」を数える(出現中の敵は数え、待ちの敵は数えない)、(b) スロットごとの待ちタイマー(4 タイルの距離判定、最大 2.0 s、重なりは押し出さない。delta で進み、ポーズで止まる)、(c) 波ごとの「全員が出現中に入った」判定と、K/T を調べ始める時点を 1 か所に置く(D-007 の継ぎ目)。 |
| 2 | 部屋のコードと敵コントローラの分離 | 模擬上の前提 | 結合していると仮定し、状態追加(2.2)と部屋・波(2.1)は直列で作る。波の出現と部屋の終了条件の結合の強さも、記述に答えがない。 |
| 3 | 接触の判定形状、レーン幅の元の値 | 模擬上の前提 | 敵の接触判定の大きさは 1 つの値で、形状は不明。スイープで扱い、円でなければ相対移動 0.25 タイル以下に分割する。レーン幅はその 1 つの値から取る。 |
| 4 | Spitter の弾(壁で消える、敵を通り抜ける) | 模擬上の前提 | 弾は仕様 §2.1 のとおりに動く。弾の仕組みは作り直さない。 |
| 5 | 視覚の仕組み | 模擬上の前提 | 必須要素 1〜6 は仕様どおり実現できる。縮小案(視覚仕様 §11)は使わない(段階 0)。敵の HP 表示はない前提。粒子は新規の 1 種を足す。レーンの赤橙と、Spitter の弾・ランタンの色の近さは未確認。 |
| 7 | 敵の挙動が経過時間で進むか | 一部確認 / 一部模擬上の前提 | 確認(模擬のコード): 可変 delta、30/60 FPS、Flinch 0.2 s、無敵 0.25 s と 0.8 s の秒指定。模擬上の前提: 既存の敵の他のタイマー(噛みつきの間隔など)が delta で進んでいるか。時間ベースと仮定し、既存のコードは直さない。 |

- 項目 6(接触結果の通知)は前提ではなく、この変更で足すもの(2.2 の接触結果、D-007 の 6)。
- 項目 1〜5 と 7 の前提が外れた場合の戻し先は、Handoff 17 と D-007 の 2 のとおり(分類 (i)〜(iv))。崩れた項目は、模擬の範囲では見つかっていない。これは実コードでの確認ではない。
- 記述から確認できた事実(根拠): 敵が共通コントローラで Idle / Chase / Attack を持ち、種別ごとの挙動がデータであること。Flinch 0.2 s が Attack を含む何でも中断すること。無敵が 1 つのフラグで、2 つのタイマーがそれぞれ切ること。移動は壁で止まること。可変 delta で 30/60 FPS をサポートすること。

### E. 実装していない・確認していないこと

- コードの変更、ビルド、テストの作成と実行は行っていない(D-008)。この文書は変更内容の記述だけである。
- 実機のゲームパッドの操作感、0.7 s の予告を読んでダッシュまで入力できるか、暗い床や小さい画面での読み取り(H1〜H4)は確認していない。
- 敵の接触判定の形状と大きさ、スロット座標の実数値、プレイヤーの移動速度、攻撃の届く距離は不明のままで、決めていない。スロット座標は、各部屋で仕様の意味(奥、左右の側面、奥の左右の隅)に対応する位置にあるとして扱う。
- 欠陥 D(被弾直後のダッシュ中のダメージ)には触れておらず、原因は推測していない。V3、V4 の測定は、直前 0.8 s 以内に被弾していない状態で行う前提のまま。
- 不確定な 1 点: 2 体の突進型が同じ更新で Windup の条件を満たす場合(部屋 5 の波 2 の L と R)、どちらが先に Windup に入るかは既存の敵の更新順で決まる。仕様に規則がなく、この変更も規則を足さない。V5(同時 1 体)には影響しない。
- 音、新しい入力ボタン、Spitter の変化、新しい敵、プレイヤー側の数値やキットの変更は含めない。

## Decisions already made

- D-001〜D-006: 戦闘の方向、Grub 突進、技術方針、怯み・接触、予告の視覚。
- D-007: 前提の台帳。
- D-008: Build は記述の完了で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- すべての結果は模擬ビルドに基づく(D-008)。実機の証拠ではない。
- 規則は決めていない。仕様と数値は変えていない。新しい入力ボタンなし。
- 無敵のタイマーのコードには触れない。欠陥 D の原因は推測しない。

## Open questions

- Handoff 22 の記述と D-009 の間に、1 文の統合以外の食い違いは見つからなかった。`outcome: question` にする必要はない。確認した点:
  - Handoff 22 の 2.1 は、調べ始める時点を未決として未反映にしていた。この点は D-009 の 1 文で置き換えた。
  - Handoff 22 の待ちの記述に「いったん終わったスロットは待ち直さない」がなかった。これは `design/combat.md` §4.1 と D-009 に既にある文面なので、2.1 に写した。規則の追加ではない。
  - `design/combat.md` §4.3 の表は、K/T を波 2 の行に置いている。その注記は「その波の次の波を出す条件」とも読めるが、括弧内の「波 1 の全員が出現中に入った時点から調べる」と V12(a)(b)から、波 2 を出す条件と読むのが自然である。この記述でもそう読んだ。表の注記の言い回しが紛らわしいだけで、規則の食い違いとは見ていない。表現の整理が要るなら `game-designer` の判断。
- 上記のほかに、Studio が `game-designer` に回すべき問いはない。

## Expected output

Studio は、この Handoff の Findings A〜E を使って Verify の Handoff を組み直す。2.3 は `art-director` 向け、2.1、2.2 と対応(B、C)は `qa` 向け。`qa` には Sender assessment を渡さない。

## Sender assessment

- 確信度: 2 章の数値と状態遷移は Handoff 22 から写し、D-009 の 1 文を `design/combat.md` §4.1 に照らして統合した。規則の追跡(B)は高い。低いのは、台帳 1〜5 の模擬上の前提(実コードでの確認なし)と、見た目の細部(レーン長の求め方、使用済み表示の描き方)。レーン長を「Charge と同じ衝突判定」で求めるのは、仕様の「壁の手前で切る」の読み方の 1 つである。
- 疑い 1: 接触の瞬間の無敵を、その更新で見えているフラグで読むため、V3 の窓の端が 30 FPS で最大 1 フレームずれうる。仕様の許容に収まる想定だが、確認していない。
- 疑い 2: 台帳 5 で、必須の視覚要素がすべて使えると置いた。使えないと分かれば、縮小案または `art-director` への戻しになる。
- 疑い 3: 台帳 1 の波の持ち方(a)〜(c)は、スポナーがない記述の上での前提である。この前提が外れても、D-007 の継ぎ目が 1 か所なので影響は局所に収まる想定。
- 範囲外は広げていない。欠陥 D の原因の推測は書いていない。

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-006-grub-charge-telegraph-visual.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/27-studio-to-gameplay-engineer.md
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

<<<FILE goals/G-001-combat-monotony/30-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 30
from: qa
to: studio
stage: Verify
outcome: question
---
# 30: qa → studio — 模擬ビルド 0.4 の V1〜V12 検証結果(pass にできない項目あり)

## Task

`sim/build-0.4.md` が `design/combat.md` の V1〜V12 を満たすかの検証結果を報告する。Studio は、下記の「未確認」と「仕様との食い違い」をどこに回すか決めてほしい。

## Context

G-001、Verify。**この報告はすべて「模擬ビルドの記述に基づく」(D-008)。実機で動かして観測した証拠ではない。** 検証は、仕様(`design/combat.md`、D-005、D-009)とビルド記述だけから行った。実装側の説明や自己評価は使っていない。

## Findings

### 総合判定

- **V1〜V12 のうち、記述から fail と言える基準はない。**
- ただし **V7 と V10 は一部が確認できず、全体を pass にできない**。そのため outcome は `pass` ではなく `question`。
- 基準 V1〜V12 の外で、**仕様とビルドの食い違いを 1 件**見つけた(F-1)。
- 同じ基準が 2 回失敗した事例はない。戻りルールは発動しない。

### 基準ごとの結果

| 基準 | 結果 | 根拠(ビルド記述) |
|---|---|---|
| V1 Windup 0.7 s、予告なしの Charge なし | pass(模擬) | 突進の手順は Wind-up 0.7 s → Charge → Recovery の固定順。出現直後は「出現中が終わって 1.5 s 以上」が条件で、Recovery 後も同じ手順に戻る。ポーズは全タイマーを止め、復帰で大きく進まない。30/60 FPS の差は約 0.034 s 以内と明記されている。被弾中に Windup を飛ばす記述はない。 |
| V2 Charge 8 タイル/s、7 タイルまたは壁、方向固定 | pass(模擬) | 「8 tiles/s、最大 7 タイル、壁まで」「方向は固定、動いてもレーンは回らない」。全長で約 0.9 s は 7/8 s と整合する。 |
| V3 ダッシュの窓(接触の瞬間の 0.25 s 前〜接触の瞬間) | pass(模擬)。ただし窓の端の数値は未測定 | 突進の判定は「最初に重なった瞬間の無敵状態」で決まる。ダッシュの 0.25 s の保護があり、重なりの途中でダッシュが切れても被弾しない。30 FPS の端のずれは最大 1 フレーム(約 0.034 s)。「窓から 0.05 s 外れると被弾」はこの規則から論理的に導けるが、ビルド記述に数値はなく、ログにもダッシュ開始時刻の項目がない。実機で測る必要がある。直前 0.8 s 以内に被弾した場合は対象外(欠陥 D)。 |
| V4 接触ダメージは Chase と Charge のみ、突進ごとに 1 回 | pass(模擬) | 「1 回の突進で最大 1 回」「最初の重なりが決める」「開始時に重なっていれば開始の瞬間」。無敵なら通り抜け、重なりが続いても無敵が切れてもダメージなし。Windup と Recovery の重なりは何も起きない。新しい突進は数え直す。 |
| V5 同時の Windup/Charge は 1 体まで | pass(模擬) | 開始条件に「他の生きている突進型が Windup または Charge 中でない」がある。倒れた Grub のレーンは 0.1 s 以内に消え、別の Grub が Windup を始められる。2 体が同時に条件を満たすと、どちらが先かは予測できないが、1 体ずつになる。 |
| V6 突進スイッチ | pass(模擬) | 「オフにすると突進型がすべて通常型になる(隆起なし、突進なし)」。敵の数、波、出現位置は同じとある。 |
| V7 部屋構成、K/T、速度、間隔、遠い方 | **一部未確認** | 下の「V7 詳細」を参照。 |
| V8 出現中 0.8 s、押し出さない | pass(模擬) | 「0.8 s フェードイン。動かず、攻撃せず、ダメージを与えず、こちらの攻撃も効かない」「押し出されず、敵がプレイヤーの上に出ることもある」。 |
| V9 Spitter の最初の弾、弾速、弾の挙動 | pass(模擬) | 出現中が終わってから 1.0 s で最初の 1 発。4 タイル/s、撃った瞬間の位置へ直進、1 ハート、壁で消える、敵を通り抜けて敵に当たらない。部屋ごとの間隔は V7 参照。 |
| V10 プレイヤー側の数値が変わっていない | **未確認** | ビルド記述に書かれているプレイヤー側の数値はダッシュの 0.25 s の保護だけで、仕様と整合する。攻撃の回復 0.35 s、ダッシュのクールダウン 0.6 s、被弾の硬直 0.3 s と無敵 0.8 s については、変更したという記述も変更していないという記述もない。記述がないことを pass の根拠にはしない。実機での測定が必要。 |
| V11 突進型の Windup/Charge/Recovery で怯まない | pass(模擬) | 3 状態では HP だけ減り、怯まず、押し戻されず、方向、速度、タイミングも変わらない。HP 0 ならどの状態でも即死。Chase 中は 0.2 s 怯む。怯みは待ち時間を巻き戻さない。出現中は攻撃が効かない。 |
| V12 波 2 のタイミング(出現位置の待ち) | pass(模擬) | 下の「V12 詳細」を参照。 |

### V7 詳細

一致を確認できたもの:
- 部屋 1〜5 の波ごとの敵の構成とスロット。
- 部屋 1 は K=1、T=10 s、部屋 2 は K=0、T=15 s、部屋 3〜5 は K=1、T=12 s。
- 合計数と同時最大数(3/2、4/3、4/3、5/3、6/4)。
- Spitter の間隔(部屋 3 は 2.0 s、部屋 4 は 1.8 s、部屋 5 は 1.6 s)。
- 「生きている敵」に出現中を含み、待ちの敵は含まない。
- 遠い角は波を出すと決めた時点で選び、待ちの間は選び直さない。
- K/T は全員が出現中に入った時点から調べる。T の起点は部屋 1 と 2 で「最後に出現中が終わってから」と明記されている。部屋 3〜5 は一般規則に従うと読める。

**未確認(理由)**:
1. **Grub 速度の数値**。仕様は 2.0/2.0/2.2/2.2/2.4。ビルドは部屋 3 を「部屋 1〜2 より少し速い」、部屋 5 を「最も速い」としか書いておらず、部屋 4 は言及がなく、数値もない。
2. **「遠い角」の同距離のとき FL を選ぶ規則**。ビルドに記述がない。ログには選んだ角が出るが、同距離の扱いは記述から確認できない。距離を中心間で比べることも明記されていない。

### V12 詳細(Handoff 29 の補足に従う)

- (a) 部屋 2: 遠い側の突進型が待っている間は波 2 が出ない。出現中に入ってからは、倒れたとき(K=0)か、出現中が終わって 15 s たったときの早い方で出る。出現中の 0.8 s は攻撃が効かないので、最短の撃破はその後になる。出現中は「生きている」に数えるので、すぐ出ることはない。**pass**。
- (b) 部屋 1: 左だけ待たせると右の Grub が先に出現中に入り、待つ側が出現中に入るまで波 2 は出ない。待っている間に右を倒した場合は、左が出現中に入った時点で生きている敵が 1 体なので、波 2 は**すぐ出る**。ビルドの記述もそうなっていて、期待値と一致する。倒さなかった場合は 2 体なので、1 体倒すか、後から出た側の出現中が終わって 10 s で出る。**pass**。ただし記述は左だけの場合で、右だけは対称と読んだ。
- (c) 4 タイル以上離れると、その時点で出現中に入る。いったん待ちが終わったスロットは待ち直さない。全員が出現中に入るまで波 2 は出ない。**pass**。ただし、同じ波の複数スロットの待ちが「波を出すと決めた時点から同時に始まる」ことは、ビルドに明記がない(「スロットごとに別々」とだけある)。基準の結果には影響しないが、実機のログで確認したい。
- (d) 待ちがない波は、出現した時点から数え始める。**pass**。

### 退行の確認

- 部屋 1 と 3 は以前の手触り+波 2 回。ビルドの記述上、新しい挙動は波だけ。
- 通常型 Grub と Spitter の怯み 0.2 s は変わらない。
- 新しい入力ボタンなし。新しい音なし(D-001 に抵触しない)。
- 点滅は 1 秒に 3 回を超えない、と記述されている。
- 30/60 FPS は、ビルドが「同じ」と述べている点を読んだだけで、別々の観測はしていない。
- **既知の欠陥 D**: ビルドは「被弾直後にダッシュすると、ダッシュの途中でダメージを受けることがある。これは、そのときに届く突進にも当てはまる」と書いている。仕様は欠陥 D の規則を意図して書いておらず、V3、V4 の測定も被弾から 0.8 s 以上たった状態に限っている。**よって fail にはしない**。ただし、ダッシュで抜けたつもりが当たる場面が実際に起こり得る。Play の「抜けた」と感じられるか(6.2)に影響しうるので、Studio は Play の前に知っておいてほしい。期待される挙動は仕様で意図的に未定義なので、`game-designer` の判断が要る。

### 基準外の食い違い(F-1)

- **内容**: 突進の再開始の待ち時間の起点が違う。仕様 §3.3 は「**前回の Recovery が終わってから** 2.5 s 以上」。ビルドは「前回の**突進が終わってから** 2.5 s 以上」(Recovery 0.8 s を含む)。
- **影響**: ビルドだと、同じ Grub の次の突進の条件が仕様より 0.8 s 早くそろう。突進の頻度が上がる。予告(V1)、同時 1 体(V5)、ダッシュが間に合うか(§3.5。次の Windup は前の Charge の後)は壊れない。
- **重大度**: 低〜中。V1〜V12 のどれも直接は落ちない。ただし仕様の数値と違う。
- **扱い**: 意図が仕様どおりなら、ビルド側の修正が要る(`gameplay-engineer`)。ビルド側が意図なら、仕様を直すかどうかは `game-designer` の判断。QA は決めない。

## Decisions already made

- D-005: 怯み、接触、遠い方の規則。V3、V4、V7、V11 の判定の基準にした。
- D-008: 判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点。V7、V12 の判定の基準にした。

## Constraints

- この報告は模擬ビルドの記述に基づく。実機の証拠として扱わない。
- 見た目の A 系の基準は `art-director` の担当で、この報告の範囲外。
- QA は仕様の期待値を決めない。

## Open questions

1. **V7 の速度と同距離の規則、V10 の測定**: ビルド記述では確認できない。実機のビルドか、より詳しい記述が要る。`gameplay-engineer` に、各部屋の Grub 速度の数値と、遠い角が同距離のときの挙動を示してもらうのが妥当。V10 は実機でプレイヤー側の数値を測る必要がある。
2. **F-1(再開始の起点)**: ビルドを仕様に合わせるか、仕様を直すか。
3. **欠陥 D**: Play 前に規則を決めるか、既知の欠陥として Play に渡すか。

## Expected output

Studio がこの結果を読み、次を決める。
- F-1 と、V7/V10 の未確認の扱い(`gameplay-engineer` に戻すか、`game-designer` に回すか)。
- 欠陥 D を Play の前に扱うか。
- 解消後に、QA がこの報告の未確認項目と F-1 を再検証する。

## Load

- Role: none (Studio が読む)
- Skills: none
- Project: design/combat.md、sim/build-0.4.md
- Decisions: decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/29-studio-to-qa.md
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
