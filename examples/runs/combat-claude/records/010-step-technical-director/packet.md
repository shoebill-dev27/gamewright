# Studio operation packet

operation: Step
goal: G-001
role: technical-director
incoming_handoff: goals/G-001-combat-monotony/07-studio-to-technical-director.md
next_seq: 8

## You may write

- goals/G-001-combat-monotony/08-technical-director-to-<recipient>.md
- decisions/D-004-<name>.md

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

<<<FILE goals/G-001-combat-monotony/07-studio-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 7
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 07: studio → technical-director — 戦闘仕様(部屋の構成と進行、予告つき Grub 突進)の実現性を確認し、技術計画を立てる

## Task

`design/combat.md` の仕様について、既存システムでの実現性を確認し、リスク・テスト・順序・並列化可否を含む技術計画を作る。特に §9 の確認事項(状態の追加、判定の取りこぼし、波の出現、部屋データ、時間の進め方)に答える。

## Context

Goal G-001「戦闘が単調なので改善したい」。プレイテスターの観察と診断を経て、`game-director` が D-002 で方向を決めた(主軸は部屋の構成と進行、敵の挙動の追加は予告つき Grub 突進の 1 つのみ)。`game-designer` がそれを `design/combat.md` に仕様化し(Handoff 06)、D-003 で突進の規則を記録した。実装の前に、技術的な実現性を確認する段階である。突進の予告の見た目は `art-director` が別の独立したステップで扱うため、ここでは扱わない。

## Findings

仕様の概要(詳細は `design/combat.md`):

- §2〜3: 敵の共通規則(出現中 0.8 s、弾の扱い)と Grub 突進の状態・数値・規則。
- §4: 5 部屋の進行、波の規則、部屋ごとの構成表、突進スイッチをオフにした版。
- §5: 突進が他の脅威と重なったときの読みやすさの規則。
- §6: 検証の観点(qa 向け V1〜V10)。
- §7: 調整項目。§8: 未定義のまま残した項目。§9: 技術確認。§10: art への条件。
- 数値はすべて暫定値。プレイヤー側の数値とキットは変えていない。
- 設計者が挙げた確認事項は §9 にある。波の出現や状態の追加が既存システムで大きな費用になる場合の扱いは、下の Open questions を参照。

この Handoff に既存実装についての調査結果はない。コードの状態は `sim/repo-notes.md` と、ビルド 0.3 の記述(`sim/build-0.3.md`)を確認すること。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。新ボタンは Owner の承認なしでは不可。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進の 1 つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。Windup は全部屋で同じ。部屋ごとに突進スイッチで外せる(スイッチをオフにすると同じ数・同じ位置の通常 Grub に置き換わる)。

## Constraints

- デスクトップ、キーボードとゲームパッド。30 FPS と 60 FPS の両方で正しく動くこと。時間はすべて秒で定義されており、フレーム数に依存させない。
- 小さなチーム: 既存システムを再利用する変更を優先する。
- D-001、D-002、D-003 の範囲内。部屋数(5)とラン長(15–20 分)は変えない。
- 仕様を変える必要が出た場合は、技術的な判断で仕様を書き換えず、下の戻りルールで返す。
- 欠陥 D(被弾直後のダッシュ中のダメージの疑い)は別ステップ(`qa` による再現)で扱う。この計画の対象に含めない。ただし、無敵・ダッシュの判定を触る実装になる場合は、その影響を計画に記す。

## Open questions

- §9 の確認事項それぞれについて、既存システムで可能か、追加が必要か、その費用の大きさ。
- 突進スイッチと波の出現を、部屋データでどう持たせるのが最小の変更か。
- 突進の判定(最大 7.0 タイルを 8.0 タイル/s で移動)が 30 FPS でも取りこぼしなく働くか。
- 実装を並列化できるか(できる場合は分割案)。

## Expected output

- 技術計画: 確認事項への回答、技術的リスク、テスト方針(`design/combat.md` §6.1 の V1〜V10 を 30 FPS と 60 FPS で確認できること)、実装の順序、並列化の可否。置き場所は、この結果を載せる Handoff の Findings とする。
- 結果の Handoff は `to: studio` 宛てにする(`art-director` の並列ステップの完了を待って Build に進めるため、Studio が両方の結果を見てから次へ回す)。
- 仕様が実現困難・範囲外の費用になる場合は、`outcome: question` で Studio に返し、理由と代替案を書く。Studio が戻りルールに従って Design(`game-designer`)または Decide(`game-director`)へ回す。技術的な判断で仕様を書き換えない。

## Sender assessment

なし。Studio は game design や技術の判断をしていない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: design/combat.md(特に §2〜4、§6、§9)、project.md#constraints、sim/repo-notes.md、sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/06-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
---
# Role: Technical Director

## Responsibility

Turns approved specs into technically feasible plans. Owns technical risk, architecture, test
strategy, sequencing, and whether work can safely run in parallel.

## Decides

- Technical approach and architecture within the project's constraints.
- Sequencing, task breakdown, and parallelization (including isolated code workspaces).
- Technical acceptance checks (e.g., performance budgets) that serve the spec.

## Must not

- Change the spec to suit the implementation — propose the change to `game-designer`.
- Decide game direction or player-facing behavior.
- Approve its own plan's results; QA verifies the build.

## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.

## Produces

- A plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
  decision with its reason.
- Technical Decisions where a real alternative was rejected.

## Hands back / escalates when

- The spec is infeasible within constraints → `game-designer`.
- The cost or scope exceeds what the Goal implies → `game-director`.
- The work is irreversible or high-risk → Owner, via an Escalation it prepares.

## Typical skills

technical-plan, make-decision, prepare-owner-escalation
>>>END

<<<FILE studio/skills/technical-plan.md
---
name: technical-plan
description: Turn an approved spec (or a technical problem) into an implementation plan with affected systems, ordered tasks, risks, test strategy, and a parallelization decision.
---
# Skill: Technical plan

Typical roles: technical-director.

## When to use

The approach is non-obvious, risky, touches several systems, or could be parallelized; or a
technical problem needs diagnosis.

## Inputs

The approved spec and acceptance criteria, project constraints, the repository.

## Method

1. Map spec items to affected systems. Find what already exists and can be reused.
2. Order the tasks; mark dependencies.
3. List risks with mitigations (performance, frame-rate dependence, data compatibility, save data).
4. Define the test strategy: what is automated, what QA checks manually.
5. Decide parallelization: parallel only for code changes that are independent; give the reason
   either way. Isolated workspaces only for parallel code changes.
6. Flag anything infeasible, much costlier than the Goal implies, or irreversible.

## Output

Plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
decision, flags.

## Do not

Change the spec to make the plan easier — propose the change instead.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3 → G-001 仕様、暫定)

状態: G-001 / D-002 / D-003 に基づく仕様。**この文書の新しい数値はすべて暫定値(P)**。H1〜H4(ゲームパッドの操作感、各部屋の実時間、音と演出、敵の速度と弾速など)の実機確認後に調整する。確認前に、プレイヤー側の数値は変えない。

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
- **敵の被ダメージ**: ノックバックや怯みは仮定しない(既存のまま)。敵は攻撃を受けても、状態(予告、突進など)を中断しない。HP が 0 になれば、その時点で倒れる。

### 2.2 Spitter の数値(部屋ごと、§4 の表)

- 撃つ間隔は部屋ごとに変える。出現中が終わってから最初の 1 発までは 1.0 s(P)。
- 撃ち方(直進、1 発ずつ、先読みなし)は変えない。

## 3. Grub 突進

### 3.1 意図

Grub が立ち止まって溜め、その直線上に突っ込む。プレイヤーは予告を見て「横に出る」「ダッシュの無敵で突進を抜ける」を選ぶ。抜けたあとの隙に反撃できる。害を与える前に、必ず予告が見える(柱3)。

### 3.2 状態

| 状態 | 長さ | 動き | 接触ダメージ |
|---|---|---|---|
| Chase | 条件まで | 部屋の Grub 速度で歩く | あり(1 ハート) |
| Windup(予告) | **0.7 s (P)** | その場で停止。突進方向を **Windup の開始時に固定** | **なし** |
| Charge | 距離 7.0 タイルまたは壁まで | 固定した方向へ **8.0 タイル/s (P)** で直進(最大約 0.875 s) | あり(1 ハート) |
| Recovery(隙) | **0.8 s (P)** | その場で停止 | **なし** |

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
- **ダメージ**: Charge 中の接触で 1 ハート。1 回の突進で与えるダメージは 1 回まで。プレイヤーが無敵のとき(ダッシュ中、被弾後の 0.8 s)は、ダメージなしで Grub が通り抜けて走り続ける。
- **終了**: 7.0 タイル進むか壁に当たったら Charge が終わり、すぐ Recovery に入る。壁に当たったときの特別な処理はない。
- **Windup 中に倒された場合**: 予告はその場で消え、同時予告の枠が空く。Charge 中に倒されたときも同じ。Windup 中の攻撃は有効な対処で、Windup は中断されない。
- **ポーズ**: 状態の時間は止まる。

### 3.5 ダッシュの無敵で抜けられるか(確認)

- 止まっているプレイヤーに対して、Windup の開始時の距離が d タイルなら、突進が届くのは Windup の開始から約 0.7 + d/8 s 後。
  - d = 3 で約 1.075 s、d = 6 で約 1.45 s。
- ダッシュの無敵は 0.25 s なので、**接触の 0.25 s 前から接触の瞬間までに、ダッシュを始めれば抜けられる**。窓の幅は 0.25 s(30 FPS で約 7〜8 フレーム)。
- 横方向のダッシュなら線から出るので、窓はこれより広い。
- 連続する 2 回の突進のあいだ: 次の Windup は前の Charge が終わってから始まる。次の接触は前の接触の約 1.2 s 以上あと(d = 6 の最悪の場合)。ダッシュのクールダウンが「ダッシュの終了から 0.6 s」と読んだ最悪の場合でも、前の接触から約 0.85 s 後に再使用できる。**ダッシュが間に合わない並びは作られない。**
- 歩いて線から出られるかは、プレイヤーの移動速度(未定義)に依存する。この仕様では保証しない。歩きだけで簡単に避けられ、ダッシュを使う理由が出ない場合は §7 の調整項目で調整する(C の検証)。

### 3.6 反撃の隙

Recovery(0.8 s)は止まっていて接触ダメージもない。攻撃の回復 0.35 s なら、隣接していれば 2 回振れる(Grub の HP 2)。ただし、攻撃の届く距離は未定義なので、2 回当てられる位置取りが実機で成立するかは Play で確認する。

## 4. 部屋の進行

### 4.1 共通ルール

- 部屋の総数は 5、各部屋の敵の数は 3〜6 体のまま(既存)。
- 波(wave):
  - 次の波は、「生きている敵が K 体以下」または「前の波の出現中が終わってから T s」の、先に起きた方で出現する。
  - 部屋は、すべての波が出現し、すべての敵が倒れたときに終わる。
- 出現位置(スロット): 扉側(Door)、奥(Far)、左側面(L)、右側面(R)、奥の左隅(FL)、奥の右隅(FR)。実際の座標は部屋データ。
  - 出現の時点でプレイヤーがスロットから 4 タイル未満なら、出現を最大 2.0 s 待つ。2.0 s たったら、そのまま出現中に入る。
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
| | 2 | Spitter × 1(FL または FR)+ 突進型 Grub × 2(L, R) | K=1, T=12 s | | | |

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
- V3: 止まっているプレイヤー(d = 4)に対し、接触の 0.25 s 前〜接触の瞬間にダッシュを始めればダメージなし。窓から 0.05 s 外れると被弾。窓の端は FPS で 1 フレーム(30 FPS 基準)以上ずれない。
- V4: 接触ダメージは Chase と Charge のみ。Windup と Recovery にはない。1 回の突進のダメージは 1 回まで。プレイヤーが無敵のときは、ダメージなしで Grub が通り抜ける。
- V5: 同時に Windup または Charge の突進型は 1 体まで。倒したら枠が空く。
- V6: 突進スイッチをオフにすると、敵の数、波、出現位置は同じで、突進が一度も起きない。
- V7: 部屋 1〜5 の波の構成、条件(K, T)、Grub 速度、Spitter 間隔が §4.3 の表と一致する。
- V8: 出現中が 0.8 s。この間は行動もダメージもない。
- V9: Spitter の最初の 1 発が出現中の終了から 1.0 s、弾速 4.0 タイル/s。弾は壁で消え、敵を通り抜ける。
- V10: プレイヤー側の数値(攻撃、ダッシュ、被弾の規則)が変わっていない。

### 6.2 体験の観点(Play と Review 向け)

Playtester への handoff には書かない(基準を知らせない)。

- 立って振り続けるだけでは、後半の部屋(3〜5)で被弾するか。
- 部屋ごとに、敵の出方や対応の仕方が違うと感じるか。
- 突進の予告が、害を与える前に見えて読めるか。突進に当たったとき、「予告は見えていた」と言えるか。
- ダッシュを、移動以外の戦闘の場面で自発的に使うか。使った理由を言えるか。
- 被弾が「自分の判断ミスのせい」と感じられるか。
- 30 FPS と 60 FPS で同じに感じられるか。
- 突進オンとオフを比べて、オンの方が単調さが減るか(A、C)。

## 7. 調整項目(暫定値、H1〜H4 の確認後に調整)

先に動かす順:

1. 予告が読めない場合: Windup を 0.7 → 0.9 s に伸ばす。部屋 4、5 で同時に出る数を減らす。
2. 簡単すぎる場合: 部屋 4、5 の Grub 速度、Spitter 間隔、トリガー距離。
3. 歩きだけで避けられてダッシュを使わない場合: Charge 速度(8.0 → 10.0)、Windup(0.7 → 0.55 まで)。ただし 0.5 s を下回らない。

プレイヤー側の数値(攻撃の回復、ダッシュのクールダウンなど)は、H1 の確認後に別の判断で扱う。

## 8. 未定義のまま残す項目

- 最大ハート数: この仕様は値に依存しない。既存のビルドのまま。
- プレイヤーの移動速度、攻撃の届く距離、各敵とプレイヤーの判定の大きさ: 既存のまま。
- ダッシュのクールダウンの起点(開始か終了か): §3.5 は最悪の場合で確認済み。
- 敵どうしの歩行時の押し合い、敵の怯みとノックバック: 既存のまま、この仕様では変更しない。
- 出現位置がプレイヤーに重なった場合の押し出し: 実現性の確認事項。
- フレーム落ち(30 FPS 未満)時の挙動: サポート外。
- 欠陥 D(被弾直後のダッシュ中のダメージ)の規則: `qa` の再現結果が出てから書き足す。この仕様には含めない。
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

## 10. art-director に渡す条件

見た目の具体案は art-director が決める。仕様として求める条件:

- **突進の予告**: Windup の 0.7 s の間ずっと見える。突進が来ることと、その方向がわかる。通常の Grub の歩きと見分けがつく。色だけに頼らない。音だけに頼らない。音を付ける場合は、Windup の開始に合わせる。
- 長さは時間(0.7 s)で決まり、30 FPS と 60 FPS で同じ長さに見える。
- Charge 中は、歩きや Windup と見分けがつく。Recovery 中は、「止まっていて攻撃が通る」とわかる。
- 突進の予告が、Spitter の弾、出現中の表示、他の敵の動きと重なっても、読める。
- 出現中(0.8 s)が、行動する敵と見分けがつく。
- 突進型の Grub が、出現時から通常型と見分けがつくかどうかは、art-director が判断する。

## Rooms(旧記述)

旧: 5 部屋、各 3〜6 体、Grub と Spitter の混成。部屋は全敵撃破で終わる。→ §4 に置き換え。

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE goals/G-001-combat-monotony/06-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 6
from: game-designer
to: studio
stage: Route
outcome: done
---
# 06: game-designer → studio — 部屋の構成と進行、予告つき Grub 突進の仕様ができた。技術確認と見た目の条件を回す

## Task

`design/combat.md` の仕様(D-002 に沿った 5 部屋の構成と進行、予告つき Grub 突進)を受け取り、次の宛先を決める。実装の前に `technical-director`(実現性)と `art-director`(予告の見た目)に回し、そのあと実装、`qa`、Play に進む。

## Context

Goal G-001 の依頼は「戦闘が単調なので改善したい」。`game-director` が D-002 で方向(案2を主、案1は予告つき Grub 突進の 1 つのみ)を決め、仕様化(`write-design-spec`)が回ってきた。この handoff はその結果。

## Findings

**書いたもの**

- `design/combat.md` を更新。プレイヤー側の数値は変えていない。内容は次のとおり。
  - §2〜3: 敵の共通規則(出現中 0.8 s、弾の扱い)と Grub 突進の状態・数値・規則・ダッシュで抜けられるかの確認。
  - §4: 5 部屋の進行の筋、波の規則、部屋ごとの構成表、突進を外した版。
  - §5: 突進が他の脅威と重なったときの読みやすさの規則。
  - §6: 検証(qa 向け V1〜V10、体験の観点)。
  - §7: 調整項目。§8: 未定義のまま残す項目。§9: 技術確認。§10: art への条件。
- `decisions/D-003-grub-charge-and-room-rules.md`: 突進の規則(同時 1 体、方向固定、予告中は無害、Windup は全部屋で同じ、部屋ごとのスイッチ)を記録。

**主な数値(すべて暫定値)**

- 突進: Windup 0.7 s、Charge 8.0 タイル/s で最大 7.0 タイル、Recovery 0.8 s。再突進の間隔は 2.5 s。
- 突進は部屋 2、4、5 に入れる。部屋 1 と 3 には入れない。
- Grub 速度は部屋 1〜5 で 2.0 / 2.0 / 2.2 / 2.2 / 2.4 タイル/s。
- Spitter 間隔は部屋 3〜5 で 2.0 / 1.8 / 1.6 s。弾速 4.0 タイル/s(全部屋)。
- 敵の合計は 3 / 4 / 4 / 5 / 6 体。既存の「3〜6 体」の範囲内。

**Open questions への回答**

1. 5 部屋の進行の筋: 基本 → 突進を読む → Spitter → 突進と弾の組み合わせ → 全部入り(§4.2)。
2. 突進は部屋 2、4、5。突進スイッチをオフにすると、同じ数・同じ位置の通常 Grub に置き換わり、どの部屋も成立する(§4.5)。
3. 予告 0.7 s、突進 8.0 タイル/s・7.0 タイル、隙 0.8 s。ダッシュの無敵(0.25 s)で抜けられる。接触の 0.25 s 前から接触の瞬間までにダッシュを始めればよい。連続する突進でも、ダッシュのクールダウンが間に合う並びだけが作られる(§3.5)。歩いて避けられるかはプレイヤーの移動速度(未定義)に依存し、保証しない。
4. 同時に予告できる突進は 1 体まで。Windup は全部屋で 0.7 s。予告中の Grub は無害。弾は遅い(§5)。読めるかは実機で確認する必要がある。
5. 実現性の確認が要る点は §9、art に渡す条件は §10。
6. 検証の観点は §6。診断の 6 項目を引き継いだ。

**routing の依頼**

- `technical-director`: `design/combat.md` §9 の確認事項(状態の追加、判定の取りこぼし、波の出現、部屋データ、時間の進め方)。実装の前に回す。
- `art-director`: §10 の条件(予告の見た目と音、Charge、Recovery、出現中の見分け方)。技術確認と並行してよい。
- 欠陥 D は別の流れ(2b)。`qa` の再現結果が出てから、設計書に書き足す。この仕様に含まれていない。
- Playtester に渡す handoff には、仕様の数値や §6.2 の体験の観点を書かないこと。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。
- D-002: 主軸は部屋の構成と進行。併用は予告つき Grub 突進の 1 つのみ。
- D-003(今回): 突進の規則と部屋の突進スイッチ(game-designer の権限内)。

## Constraints

- D-001、D-002 の範囲内。新しい敵の種類、Spitter の撃ち方の変化、プレイヤー側の数値やキットの変更、部屋数、ラン長は変えていない。
- 時間はすべて秒。30 FPS と 60 FPS で同じ長さ。
- 技術的な方法と見た目の具体案は決めていない。

## Open questions

方向や優先度に関わる選択は出ていない。次は他の Role の判断を待つ。

- 技術確認で、波の出現や状態の追加が既存のシステムで大きな費用になる場合は、仕様を変えるか `game-director` に回す。
- 予告が弾や他の敵と重なって読めない場合は、Play の後で §7 の順に調整する。

## Expected output

- Studio が `technical-director` と `art-director` に回す。結果を受けて、必要なら仕様を修正する(`game-designer`)。
- そのあと、実装 → `qa`(§6.1 の V1〜V10、30 FPS と 60 FPS) → Play(H1〜H4 の実機確認を含む) → Review。
- 突進オンとオフの比較は、Play で行う。

## Sender assessment

- 確信度: 構成と進行は中〜高。突進の効果と、予告の読みやすさ(特に部屋 4、5 の重なり)は、実機で見るまで中程度。
- 数値(Windup 0.7 s、Charge 8.0、Recovery 0.8 など)は、反応時間と性質の推定で置いた暫定値。H1〜H4 の確認前なので、固定しない。
- 歩きだけで避けられる場合、ダッシュを使う理由が出ない可能性がある(C)。その場合の調整は §7 に書いた。
- Windup 中の攻撃で突進を無効にする対処が簡単すぎる可能性がある。Play で見る。
- Owner のエスカレーションは不要(D-001 も柱1の解釈も変えていない)。

## Load

- Role: none(Studio の routing)
- Skills: none
- Project: design/combat.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/05-game-director-to-game-designer.md
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
