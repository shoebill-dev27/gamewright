# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/43-studio-to-game-director.md
next_seq: 44

## You may write

- goals/G-001-combat-monotony/44-game-director-to-<recipient>.md
- decisions/D-010-<name>.md

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

<<<FILE goals/G-001-combat-monotony/43-studio-to-game-director.md
---
kind: handoff
goal: G-001
seq: 43
from: studio
to: game-director
stage: Review
outcome: routed
---
# 43: studio → game-director — 模擬ビルド 0.6 に基づく Goal G-001 の Review

## Task

模擬ビルド 0.6 について、Goal G-001(戦闘の単調さの改善)の意図が満たされたかを判定する(`review-outcome`)。満たされていなければ、次の課題を挙げて Diagnose に戻す材料にする。判定は模擬ビルドに基づく旨を明記する。

## Context

- Owner の依頼は「戦闘が単調なので改善したい」。成功条件は、想定プレイヤーが戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること(`goals/G-001-combat-monotony/goal.md`の Interpretation)。
- 方向は D-002 で決まった。主軸は部屋の構成と進行(波)、併用は予告つき Grub 突進の 1 つだけ。
- Owner の判断(D-008): 本プロジェクトは模擬専用のサンプルで、判定は模擬ビルド(`sim/build-0.6.md`)に基づいて行う。結果には模擬であることを明記する。
- ここまでの経過: Build は完了。Verify は `qa`(V1〜V12。Handoff 38)が pass、`art-director`(視覚。Handoff 40)が pass で、いずれも模擬ビルドの記述に基づく。Play は Playtester が実施した(Handoff 42)。

## Findings

Playtester の観察報告(Handoff 42)の要点。全文は Load の Handoff 42 を読むこと。

**観察の性質(判定の重みづけに必要)**
- 実機ではなく、`sim/build-0.6.md` の「プレイヤーに見える記述」を読んで体験を思い描いた報告である。実時間の感触、画面での見え方、ゲームパッドの操作感、音、30/60 FPS の差は確認できていない。

**よかった点(Playtester の観察)**
- 突進の予告(レーン、しゃがみ込み、色)があり、見てから避けられる。
- 背中の隆起で突進する個体を見分けられる。
- 既存の操作(移動、ダッシュ)だけで対応でき、新しいボタンは要らない。
- 突進は同時に 1 体だけ。
- 突進後の回復(0.8 秒)が反撃の機会として読める。
- 部屋 2・4・5 では、隅で立ち止まってスワイプするだけの戦い方は通用しない(記述の限り)。
- 突進中のスワイプで止まらないことには、フィードバックがある(白く光る、火花)。

**問題と影響度(Playtester の評価)**

| # | 内容 | 影響度 |
|---|---|---|
| A | 部屋 1、3 は戦い方が前と変わらず、第 2 波が来るだけ。変化は部屋 2、4、5 に集中 | 中(記述からの印象) |
| B | 突進 Grub に 3 タイル未満で張り付く、または 6 タイルより離れると突進が出ない。突進を見ずに済む戦い方がありうる(試していない) | 中 |
| C | 突進中のスワイプは止まらず、当たった手応えが薄そう | 低〜中(感触は未確認) |
| D | 出現点の近くに立つと敵が最大 2.0 秒出ず、次の波も遅れる。理由がプレイヤーに伝わるか不明 | 低〜中 |
| E | 被弾直後のダッシュで、途中で被ダメージ(欠陥 D。ビルド記述にある既知の挙動)。突進を避けるダッシュに影響しうる(実際に起きるかは未確認) | 高になりうる |
| F | 部屋 5 は敵が重なり、2 体の突進 Grub のどちらが先か読めない。公平な難しさか運任せかは未確認 | 不明 |

**Playtester の仮説(観察とは別)**
- 部屋 2、4、5 での「立ち止まりスワイプの無効化」が単調さを減らしている可能性がある。ただし実時間で遊ばないと言えない。
- 「近づき過ぎると突進しない」性質が、新しい単調さ(張り付き戦法)を生むかもしれない。

**未解決の疑問(Playtester)**
- 張り付いたとき、予告なしに突進されることはないか。
- 被弾直後のダッシュでの途中被弾は、どのくらいの頻度か。
- 出現を待たされているとき、画面でそれと分かるか。
- 部屋 5 の 2 体の突進 Grub は、どちらが先か読めるか。

**欠陥 D の扱い(process 上の事実)**
- 欠陥 D(被弾直後のダッシュ中にダメージを受けることがある)は未再現である。再現(`qa`)には Owner の元の報告文が必要だが、入力にないため `qa` の Handoff は作っていない。ルールは `design/combat.md` で意図的に未定義。Review ではこれを「未再現の既知の疑い」として扱い、次の課題に挙げる(Goal の route 表 7e と 9)。

**他の Verify 結果(Load 参照)**
- Handoff 38(`qa`): pass。V1〜V12、F-1、V10、V12(c) に食い違いなし(模擬ビルドの記述に基づく)。実機でしか確認できない点: V3 の窓の端の数値、30/60 FPS の実測、等距離でのログ確認。
- Handoff 40(`art-director`): pass。A1〜A13 に fail なし。実機要の点(暗い床での 35% のレーン、レーンと弾・ランタイムの光の区別、0.7 秒の十分さ、Recovery の誤読、かすりの感触、抜けた合図の過剰、小さい画面での尾根、30/60 FPS、色覚の差)と、ビルド記述の欠落 G1〜G5、懸念 S1〜S3 が残る。

## Decisions already made

- D-001: 攻撃とダッシュのワンボタン戦闘。新ボタンは Owner 承認なしでは不可。
- D-002: 主軸は部屋の構成と進行。敵の挙動追加は予告つき Grub 突進の 1 つに限る。
- D-003、D-005、D-009: Grub 突進と部屋・波の規則。
- D-004、D-007: 技術方針。
- D-006: 突進の予告の見た目。赤橙は害になる状態だけに使う。
- D-008(Owner): 判定は模擬ビルドに基づく。結果に模擬であることを明記する。

## Constraints

- 判定は `sim/build-0.6.md` の記述と、それに基づく Verify・Play の報告に基づく。実機で確かめたかのように書かない。
- 新しい入力ボタン、D-001 の変更、ビジョンの柱の変更を要する方向が必要だと分かったら、決めずにエスカレーションの準備(`prepare-owner-escalation`)に回す。
- 欠陥 D は Goal の範囲外。扱いは次の課題として挙げるにとどめ、ここで規則を決めない(規則は `game-designer` が 2b の再現結果を見て書く、という既存の指示)。
- 体験の観察は記述から思い描いたもので、実際の感触ではない。この限界を判定の確信度に反映する。

## Open questions

1. 模擬ビルドに基づく範囲で、Goal の意図(戦闘中に判断を実感できる)は満たされたか。`goal-met` / `goal-not-met` のどちらか。
2. 問題 A(部屋 1、3 に変化がない)、B(張り付き・離れすぎで突進を見ずに済む)、F(部屋 5 の突進順序)は、D-002 の範囲で許容する設計の帰結か、次の課題か。
3. 欠陥 D(問題 E)が、判定にどう影響するか。次の課題の優先度をどうするか。
4. 実機でしか確認できない点のうち、Goal の判定に実質的に影響するのはどれか。Outcome の「確認できない点」に何を残すか。

## Expected output

- Handoff 44(`to: studio`)。`outcome` は `goal-met` または `goal-not-met`。Findings に判定、理由、模擬ビルドに基づく旨、確認できていない点、次の課題(新しい Goal として提案する形)を書く。
- 判定が `goal-not-met` の場合は、Diagnose に戻すための要点(どの問題が主因か)を添える。
- 方向の選択を伴う判断は `make-decision` で Decision(次の番号 D-010)として記録する。
- Owner の判断が要る場合(エスカレーションの条件に当たる場合)は、決めずに `prepare-owner-escalation` で Escalation を準備する。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md, studio/skills/make-decision.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/grub-charge-telegraph.md, sim/build-0.6.md, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/38-qa-to-studio.md, goals/G-001-combat-monotony/40-art-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-008-owner-simulated-build-judgment.md, decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/42-playtester-to-studio.md
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/review-outcome.md
---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
>>>END

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE sim/build-0.6.md
# Simulated build 0.6 — what playing it looks like

A player-observable description only. Lengths are in seconds, distances in tiles, speeds in tiles per second. Everything below holds the same at 30 FPS and 60 FPS unless a difference is stated.

## Rooms and waves

- Every room sends its enemies in two waves. The first wave appears when the room starts. The second wave appears when the number of living enemies drops to the room's threshold, or when the room's timer runs out, whichever happens first.
- Enemies that are fading in count as living. Enemies still waiting to appear do not count.
- The timer starts when the last enemy of the earlier wave has finished fading in. If that enemy had to wait at its spot first, the timer starts after the wait and the fade-in.
- Each room has six spots where enemies appear: the door side, the far side (back middle), the left side, the right side, the far-left corner and the far-right corner. There is no spot in a near corner by the door. The only corners enemies appear in are the two far corners.
- Room 1: wave 1 is two ordinary Grubs, left and right. Wave 2 is one ordinary Grub at the far side. It comes when one or fewer enemies are alive, or 10 s after the last wave-1 Grub finished fading in. 3 enemies in total, at most 2 at once. No charging Grubs.
- Room 2: wave 1 is one charging Grub at the far side. Wave 2 is two ordinary Grubs (left, right) and one more charging Grub (far side). It comes when no enemy is alive, or 15 s after the wave-1 Grub finished fading in. 4 enemies in total, at most 3 at once.
- Room 3: wave 1 is a Spitter at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in whichever far corner (far-left or far-right) is farther from you at the moment the wave is triggered, and an ordinary Grub on the right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 4 enemies in total, at most 3 at once. Spitters fire every 2.0 s. No charging Grubs.
- Room 4: wave 1 is a Spitter in the far-left corner, a charging Grub at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in the far-right corner and a charging Grub on the right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 5 enemies in total, at most 3 at once. Spitters fire every 1.8 s.
- Room 5: wave 1 is a Spitter at the far side and two ordinary Grubs, left and right. Wave 2 is a Spitter in the farther of the far-left and far-right corners (chosen as in room 3) and two charging Grubs, left and right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 6 enemies in total, at most 4 at once. Spitters fire every 1.6 s.
- A room ends when every wave has appeared and every enemy is dead.
- The farther-corner choice (rooms 3 and 5, wave 2) is made when the wave is triggered, before any waiting, using where you stand at that moment. The far-left corner and the far-right corner are compared by distance from the center of you to the center of each spot, and the one with the greater distance gets the Spitter. If the two distances are exactly equal, the far-left corner is used. It is never a near corner, because there is none. If you move while the wave waits, the choice does not change. A corner that a room names for a specific enemy is not part of this choice.

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
- The farther-corner choice gives the same result at 30 and 60 FPS for the same positions.
- Pausing freezes all timers and animations, including lanes, steam and rings. Resuming after a long pause does not skip ahead more than a short step (0.05 s).
- Nothing flashes more than three times per second, apart from single flashes.

## What play feels like now

- Rooms 1 and 3 behave like before but with two waves, so there is a second arrival to deal with.
- In rooms 2, 4 and 5, standing still in a corner and swiping no longer works: a lane appears, and about 0.7 s later a Grub runs the length of it. Moving off the lane or dashing through the Grub avoids damage. Swiping the Grub during the run only chips it and does not stop it.
- A single charging Grub charges again about 3.3 s or more after its previous charge ended, and later if you are out of the 3.0–6.0 range or another one is busy.
- Only one charging Grub is ever winding up or charging at a time.
- In rooms 3 and 5, the second-wave Spitter appears in the far corner that is farther from you when the wave is triggered; if you stand exactly equally far from both, it appears in the far-left corner.
- No new sounds. No new buttons.
- As before, occasionally, if you dash right after being hit, you take damage partway through the dash. This also applies to a charge that reaches you at that moment.

## Development build only

- A tester can pick room 1–5, switch charging Grubs on or off per room (off turns every charging Grub into an ordinary Grub, with no ridge, no lane and no charge; the room's counts, waves and spots stay the same), and switch between 30 and 60 FPS.
- A log lists state changes with game time, enemy and type, charge direction, contact result (unresolved, slipped through, hit), wave arrivals with spots, the distance to you when a wind-up began, and the moment all enemies of a wave have begun fading in. For the farther-corner choice, the log shows which corner was chosen: far-left or far-right.
- The log also records the time each charging Grub's recovery ended and it went back to walking, so the gap to its next wind-up can be read directly.
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-10
---
# G-001: 戦闘の単調さの改善

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

体験上の Goal。ビルド 0.3 の戦闘が、想定プレイヤー(短時間で濃いランを求め、回避と間合いに慣れたアクション好き)にとって単調に感じられない状態にする。
成功条件は質的なもので、プレイヤーが戦闘中に、ほぼ同じ行動の繰り返しではなく、状況に応じた位置取り・タイミング・敵の挙動への対応といった判断を実感できること。数値基準は Design の受け入れ基準で、最終判定は Review で決める。

Owner の判断(D-008): このプロジェクトは模擬専用のサンプルとして扱い、`sim/repo-notes.md` をコードとする。Build は変更内容を Handoff に正確に書いた時点で完了で、模擬ビルドはランタイムのシミュレーターがその変更内容から作る。Goal の判定は模擬ビルドに基づいて行い、結果には模擬であることを明記する。

範囲外:
- 新しい入力ボタンの追加(D-001 により Owner 承認なしでは不可)。
- 戦闘以外のシステムの変更。
- ラン長(15–20分)やビジョンの柱の変更。
- 原因の特定前に解決策を決めること。

## Unknowns

Project Context の確認結果:
- ビジョンの柱 1「ワンボタン戦闘」(D-001)は、攻撃とダッシュだけのキットで、深みは位置取り・タイミング・敵の挙動から生むと定めている。「単調」の解決策はこの枠内に収める必要がある。
- 現状はビルド 0.3(5部屋、敵2種、攻撃とダッシュ)。
- 即時エスカレーションは不要。Goal は再解釈を要さず、ビジョンや既存の Decision と衝突しない。ただし方向の決定で D-001 の変更や新ボタンが必要と分かれば、その時点でエスカレーションする。

各ステージの入口の問い:
- Observe: 単調さを実際にプレイして観察したか → 観察済み(Handoff 02)。ただし被弾直後のダッシュ中ダメージの疑い(問題 D)は未再現で、`qa` による再現が必要。
- Diagnose: 原因は分かっているか → 診断済み(Handoff 04。主因は敵挙動が各1種類で単純なこと(P1)と、部屋構成に進行がないこと(P2))。感触・実時間・演出・数値に関わる仮説 H1〜H4 は未確認。
- Decide: 方向・優先度・スコープの本当の選択があるか → あった。診断が D-001 の枠内の3案(敵の挙動 / 部屋の構成 / プレイヤー数値)を示し、`game-director` が D-002 で決めた(主軸は部屋の構成と進行、併用は予告つき Grub 突進の1つのみ)。コードのない環境での Build の進め方は Owner が D-008 で決めた。
- Design: 意図する挙動は仕様化済みか → 戦闘仕様は `design/combat.md` に仕様化済みで、技術確認で出た食い違い 3 点も D-005 で解消済み(Handoff 10)。突進の予告の見た目も `design/grub-charge-telegraph.md` と D-006 で仕様化済み(Handoff 12)。Build の記述中に見つかった、波の条件を調べ始める時点の未定義は D-009 で解消済み(Handoff 24)。
- Plan: 技術的アプローチは非自明か → 実現性確認は完了(Handoff 08、D-004)。T0 は D-007 で「前提の台帳」に置き換え済み。コードにアクセスできない問題は Owner の回答(D-008)で解消し、`sim/repo-notes.md` をコードとして扱う。
- Build: ゲームを変更する必要があるか → ある(D-002)。D-008 により、変更内容を Handoff に正確に書くことで完了とする。
- Verify: Build の後は常に必要。対象は模擬ビルド。
- Play: Goal は遊び心地に関する → 変更後に必要。対象は模擬ビルド。H1〜H4 は実機では確認できないため、Outcome に限界として書く。
- Review: 体験の Goal かつ方向 Decision がある → 必要。模擬ビルドに基づく判定であることを明記する。

スキップしたステージ: なし。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [02-playtester-to-studio.md](02-playtester-to-studio.md)(開始 Handoff: [01-studio-to-playtester.md](01-studio-to-playtester.md)) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md)(開始 Handoff: [03-studio-to-game-designer.md](03-studio-to-game-designer.md)) |
| 2b | Observe(欠陥 D) | qa | reproduce-defect | planned(Escalation の答えに依存しない。Owner の報告の原文が入力にないため Handoff は未作成。後続の Studio 操作で作成。他のステップと独立。Play の前提ではない: 7e 参照。Review 後の次の課題の候補) | —(次の空き seq で `NN-studio-to-qa.md`) |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done(D-002) | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md)(出力: [05-game-director-to-game-designer.md](05-game-director-to-game-designer.md)、`decisions/D-002-combat-direction-rooms-and-grub-charge.md`) |
| 4 | Design(戦闘仕様) | game-designer | write-design-spec | done(`design/combat.md`、D-003) | [05-game-director-to-game-designer.md](05-game-director-to-game-designer.md)(出力: [06-game-designer-to-studio.md](06-game-designer-to-studio.md)) |
| 5a | Plan(実現性確認) | technical-director | technical-plan | done(D-004。仕様は実現可能。確認依頼 3 点あり) | [07-studio-to-technical-director.md](07-studio-to-technical-director.md)(出力: [08-technical-director-to-studio.md](08-technical-director-to-studio.md)) |
| 5b | Design(突進の予告の見た目) | art-director | write-design-spec, make-decision | done(`design/grub-charge-telegraph.md`、D-006。戦闘の規則の変更なし) | [11-studio-to-art-director.md](11-studio-to-art-director.md)(出力: [12-art-director-to-studio.md](12-art-director-to-studio.md)) |
| 5c | Design(仕様の確認: 怯み・接触の定義・部屋 5 の FL/FR) | game-designer | write-design-spec, make-decision | done(D-005。方向・スコープの変更なし) | [09-studio-to-game-designer.md](09-studio-to-game-designer.md)(出力: [10-game-designer-to-studio.md](10-game-designer-to-studio.md)) |
| 6 | Build(1 回目) | gameplay-engineer | implement-change | done(`outcome: question`。T0 を完了できず、実装なし) | [13-studio-to-gameplay-engineer.md](13-studio-to-gameplay-engineer.md)(出力: [14-gameplay-engineer-to-studio.md](14-gameplay-engineer-to-studio.md)) |
| 6a | Plan(T0 を実施できない場合の進め方の再確認) | technical-director | technical-plan, make-decision | done(D-007。T0 を前提の台帳に置き換え、方針 D-004 は維持) | [15-studio-to-technical-director.md](15-studio-to-technical-director.md)(出力: [16-technical-director-to-studio.md](16-technical-director-to-studio.md)) |
| 6b | Build(再開) | gameplay-engineer | implement-change | done(`outcome: question`。コードを読み書きできず、台帳のプローブも実装もできなかった。D-007 の 7 に該当し、再試行せず返した) | [17-studio-to-gameplay-engineer.md](17-studio-to-gameplay-engineer.md)(出力: [18-gameplay-engineer-to-studio.md](18-gameplay-engineer-to-studio.md)) |
| 6c | Plan(コードにアクセスできない Build の進め方、Owner 確認の要否) | technical-director | technical-plan, prepare-owner-escalation, make-decision | done(Owner の判断が必要と判断し Escalation を作成) | [19-studio-to-technical-director.md](19-studio-to-technical-director.md)(出力: [20-technical-director-to-owner.md](20-technical-director-to-owner.md)) |
| 6d | Decide(Owner) | owner | — | done(D-008。Owner は Option C を選択。`sim/repo-notes.md` をコードとして扱い、Build は変更内容の記述で完了、判定は模擬ビルドに基づく) | [20-technical-director-to-owner.md](20-technical-director-to-owner.md)(Decision: `decisions/D-008-owner-simulated-build-judgment.md`) |
| 6e | Build(変更内容の記述。D-008 により、記述の完了で Build 完了) | gameplay-engineer | implement-change | done(`outcome: question`。変更内容は 1 点を除き完了。波 2 以降の条件を調べ始める時点が仕様に未定義) | [21-studio-to-gameplay-engineer.md](21-studio-to-gameplay-engineer.md)(出力: [22-gameplay-engineer-to-studio.md](22-gameplay-engineer-to-studio.md)) |
| 6f | Design(波の条件の欠落 + §10 の参照追記) | game-designer | write-design-spec, make-decision | done(D-009。案 A: 前の波の全員が出現中に入った時点から K・T を調べ始め、待ちの敵は数えない。§10 の参照追記も完了。数値の変更なし) | [23-studio-to-game-designer.md](23-studio-to-game-designer.md)(出力: [24-game-designer-to-studio.md](24-game-designer-to-studio.md)) |
| 6g | Build(記述の確定: 2.1 に 1 文を足す) | gameplay-engineer | implement-change | done(`outcome: question`。Handoff 25 の Load に Handoff 22 が入っておらず、記述の全体を書けなかった。Studio の Load の漏れで、仕様の問題ではない。規則の追跡(V7、V12)は Handoff 26 に下書きとして残った) | [25-studio-to-gameplay-engineer.md](25-studio-to-gameplay-engineer.md)(出力: [26-gameplay-engineer-to-studio.md](26-gameplay-engineer-to-studio.md)) |
| 6h | Build(記述の確定のやり直し。Handoff 22 を Load に加えた) | gameplay-engineer | implement-change | done(`outcome: done`。変更内容 2.1〜2.4 に D-009 の 1 文を統合し、自己完結で確定。台帳 1〜5、7 の一部は模擬上の前提として明記。仕様との食い違いなし) | [27-studio-to-gameplay-engineer.md](27-studio-to-gameplay-engineer.md)(出力: [28-gameplay-engineer-to-studio.md](28-gameplay-engineer-to-studio.md)) |
| 7a | Verify(模擬ビルド 0.4。V1〜V12) | qa | verify-change | done(`outcome: question`。fail なし。V7(Grub 速度、同距離の遠い角)と V10 は記述から確認できず pass にできない。基準外の食い違い F-1(再開始の起点)あり。すべて模擬ビルドの記述に基づく) | [29-studio-to-qa.md](29-studio-to-qa.md)(出力: [30-qa-to-studio.md](30-qa-to-studio.md)) |
| 7b | Verify(視覚。7a と並列: visual-review) | art-director | visual-review | done(`outcome: pass`。模擬ビルド 0.6 の記述に基づく。A1〜A13 に fail なし。A5 と A9・A10・A11 の一部は確認不能(実機要)または記述なし。赤橙の使い方は D-006 に反しない。新しい Decision なし。懸念 S1〜S3 は Play で確認する) | [39-studio-to-art-director.md](39-studio-to-art-director.md)(出力: [40-art-director-to-studio.md](40-art-director-to-studio.md)) |
| 7c | Build(F-1 の修正と V7・V10 の明記。変更内容 2.1〜2.4 の更新) | gameplay-engineer | implement-change | done(`outcome: done`。修正後の変更内容 2.1〜2.4 の全体を自己完結で記述。F-1 の起点は Recovery 終了と明記、Grub 速度の列挙、遠い角の同距離は FL、プレイヤー側の数値は変更なしと明記。仕様の欠落・矛盾の報告なし。欠陥 D は範囲外) | [31-studio-to-gameplay-engineer.md](31-studio-to-gameplay-engineer.md)(出力: [32-gameplay-engineer-to-studio.md](32-gameplay-engineer-to-studio.md)) |
| 7d | Verify(再検証: F-1、V7、V10、V12(c)。あわせて V1〜V12 の回帰) | qa | verify-change | done(`outcome: question`。fail なし。F-1、V10、V12(c) は解消(pass、模擬)。V1〜V12 の回帰も pass(模擬)。V7 の「同距離のとき」の規則だけ、ビルドが「front-left corner」と書き、仕様の FL(奥の左隅)を指すか確認できず pass にできない。Grub 速度などV7 の他の部分は pass。欠陥 D は範囲外で、観察として記録) | [33-studio-to-qa.md](33-studio-to-qa.md)(出力: [34-qa-to-studio.md](34-qa-to-studio.md)) |
| 7f | Build(V7 の同距離の規則の用語を FL に合わせて明記。変更内容 2.1〜2.4 の更新) | gameplay-engineer | implement-change | done(`outcome: done`。修正後の変更内容 2.1〜2.4 の全体を自己完結で記述。Handoff 32 は「FL」と書いており「front-left」の語はなかったと報告。FL = 奥の左隅の対応表と、同距離は FL・手前の角のスロットは存在しない旨を明記。数値・規則・入力は変更なし。仕様の欠落・矛盾の報告なし。欠陥 D は範囲外) | [35-studio-to-gameplay-engineer.md](35-studio-to-gameplay-engineer.md)(出力: [36-gameplay-engineer-to-studio.md](36-gameplay-engineer-to-studio.md)) |
| 7g | Verify(再確認: V7 の同距離の規則だけ。他の基準が変わっていないことの確認) | qa | verify-change | done(`outcome: pass`。V7 の同距離は FL(奥の左隅)と一意に読める。手前の角は「there is none」と明記。V1〜V12、F-1、V10、V12(c) も前回から食い違いなし。すべて模擬ビルドの記述に基づく。欠陥 D は観察として記録。実機でしか確認できない点: V3 の窓の端の数値、30/60 FPS の実測、等距離でのログ確認) | [37-studio-to-qa.md](37-studio-to-qa.md)(出力: [38-qa-to-studio.md](38-qa-to-studio.md)) |
| 7e | Design(欠陥 D の扱い) | game-designer | write-design-spec, make-decision | skipped(Play の前には不要。規則は 2b の再現結果が出てから書くという Director の指示を維持する。Play では Playtester が何も知らされずに体験し、欠陥 D の挙動が「抜けた」感覚(§6.2)に影響したかを観察に基づいて報告する。Play か Review が、欠陥 D が結果の読み取りを妨げていると示した場合は、再び `game-designer` に回す) | — |
| 8 | Play(模擬ビルド 0.6) | playtester | playtest-session | done(`outcome: done`。模擬ビルドの記述を読んで思い描いた体験の報告で、実時間・見え方・操作感は確認できなかった。変化は部屋 2・4・5 に集中(A)、張り付き・離れすぎで突進を見ずに済む可能性(B)、突進中のスワイプの手応え(C)、出現待ちの伝わり(D)、欠陥 D(E。実際に起きるかは未確認)、部屋 5 の突進順序(F)。よかった点: 予告で見てから避けられる、既存の操作だけで対応できる) | [41-studio-to-playtester.md](41-studio-to-playtester.md)(出力: [42-playtester-to-studio.md](42-playtester-to-studio.md)) |
| 9 | Review(模擬ビルドに基づく判定) | game-director | review-outcome, make-decision | open(判定は模擬ビルドに基づく旨と、実機で確認できていない点を明記する。欠陥 D は未再現の既知の疑いとして、次の課題に挙げる。結果は `to: studio`) | [43-studio-to-game-director.md](43-studio-to-game-director.md) |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

- Step 1(Observe)の後: プレイテスターの観察報告(Handoff 02)は、体験の問題 A〜C(毎部屋同じ型、緊張感の欠如、ダッシュが戦闘で使われない)と、不具合の疑い D(被弾直後のダッシュ中にダメージを受けることがある)を報告した。計画どおり Diagnose(2a)に進む。
- 追加: 2b として `qa` による D の再現(`reproduce-defect`)を加えた。理由: D は仕様と食い違うか明らかな不具合の疑いであり、戻りルール(Play の結果が欠陥なら Observe は `qa`)に従う。2a の診断と互いの出力を使わない。
- 2a(Diagnose)の後: 診断(Handoff 04)は D-001 の枠内の3案を示し、方向・優先度・スコープの本当の選択があるため Decide(3)を確定し `open` にした。エスカレーションは不要と判断した。
- 3(Decide)の後: `game-director` が D-002 を記録した(主軸は案2の部屋の構成と進行、併用は予告つき Grub 突進の1つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない)。D-001 とビジョンの柱の範囲内で、新ボタンも不要なため、エスカレーションは発動しない。計画どおり Design(4)に進む。
- 3 の後の route 改訂: (a) Decide が実装前の実現性確認を求めたため、Plan(5a)を `planned` に確定した。(b) 突進の予告の見た目は `art-director` の範囲であり、Director も仕様後に回すと指示したため、Design(5b)を新設した。仕様が書き上がってから、5a と 5b を互いに独立なステップとして Handoff する(並列可。どちらも相手の出力を使わない)。(c) ゲーム変更が決まったため、Build(6)は `planned`、Verify(7)、Play(8)、Review(9)も `planned` に確定した。視覚要素(予告)が入るため、Verify は `art-director` の `visual-review` を並列に加える。
- 欠陥 D は、Director の指示どおり今回の戦闘仕様に含めない。2b の再現結果が出てから、ダッシュと被弾後の無敵の規則を設計書に書き足す。2b の Handoff は、Owner の報告の原文と設計文書のみを `qa` に渡す必要がある。報告文の原文は後続の Studio 操作で用意し、推測で書かない。
- Handoff 05 の編集(Route 手順 4–5): `stage` を `Specify` から開発ループの用語である `Design` に直した。Load に、受け手の Works from に合う `project.md#player-profile`(ゲームパッド主体のプレイヤー)と、元の観察である Handoff 02 を追加した。`Sender assessment` は触っていない。
- 観察と診断は `sim/build-0.3.md` と `design/combat.md` に基づくドライランであり、ゲームパッドの操作感・実時間・演出・数値(H1〜H4)は未確認。仕様の数値は暫定値として扱い、Play の確認後に調整する。
- 4(Design)の後: 仕様(Handoff 06)は計画どおりで、方向・優先度・スコープの選択は出ておらず、エスカレーションも発動しない(D-001、D-002 の範囲内。新ボタンなし)。Design(4)を `done` にし、Plan(5a)を `open` にした。
- 5a と 5b の Handoff について: 5a と 5b は独立で並列にできる(連続する seq で、route 番号に文字の接尾辞)。この Route 操作で書けるのは seq 7 の Handoff 1 つだけだったため、5a の Handoff(07)を先に作り、5b の Handoff は後続の Studio 操作が作る。5b の入力は `design/combat.md` §10 と `project.md#art-direction` で、`game-designer` の Sender assessment は渡さない。Handoff 06 が指示するとおり、Playtester に渡す Handoff には仕様の数値や §6.2 の体験の観点を書かない。
- 5a の Handoff(07)は Handoff 06 の Findings(客観的な仕様の内容)から Studio が組み立てた。`game-designer` の Sender assessment(確信度、暫定値の根拠)は技術計画に不要なので含めていない。
- 5a(Plan)の後: 技術計画(Handoff 08、D-004)は、仕様が D-001〜D-003 と制約の範囲で実現できると結論した。コードは読まず `sim/` の記述に基づく見積もりで、部屋データ、スポナー、弾の衝突、接触の判定形状は Build の最初の作業 T0 で確認する。`outcome: question` ではないため、Plan の戻りルール(仕様が実現不能)は適用しない。エスカレーションの条件(コンセプト・柱・Decision の変更、スコープ・費用・リスクの大幅な変化、不可逆な変更)にも当たらないと判断した。
- 5a の後の route 改訂: 技術側が仕様の文面と既存実装の食い違いを 3 点(怯みの扱い、接触の定義、部屋 5 の FL/FR)見つけ、仕様側の決定が要るため、Design(5c、`game-designer`)を新設して `open` にした(Handoff 09)。これは仕様の解釈であり、技術側は決められない。Build は 5b と 5c の両方の後に進める。5c は 5b と互いの出力を使わないので並列にできる。5c の答えが D-002 や D-003 の変更、スコープの変更を要する場合は、`game-designer` が `question` で返し、Decide(`game-director`)に回す。
- Handoff 09 の作り方(Route 手順 4–5): 受け手 `game-designer` の Works from(仕様の質問、Decision、設計文書)に合わせ、Handoff 08 の Findings から確認依頼 1〜3 と既定 4、判断材料の技術的事実だけを抜き出した。Handoff 08 の Sender assessment(欠陥 D の仮説を含む)は渡していない。欠陥 D の仮説は `qa` の再現に先入観を与えるため、2b の Handoff にも含めない。
- Handoff 08 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- Build が T2 と T3 を並列にする条件は、T0 で部屋のコードと敵のコントローラが別モジュールだと確認できること。Build の Handoff を作るときに、この条件と T0 で前提が崩れたときの Studio への戻しを Expected output に書く。Handoff 08 のとおり、開発用補助(部屋の選択、突進スイッチ、30/60 FPS 切り替え、状態の遷移ログ)は開発ビルド限定で、プレイヤー向けの新しい入力は足さない。
- 5c(Design)の後: 仕様の確認(Handoff 10、D-005)は D-001〜D-003 の範囲内で決まり、`outcome: done`。方向・優先度・スコープの変更も新ボタンもなく、エスカレーションの条件に当たらない。`game-director` に回す必要もない。5c を `done` にした。Handoff 10 の質問「欠陥 D の規則の追記」は 2b の結果待ちで、Build の前提ではない。
- 5c の後の次の操作: Build は 5b の後という計画を変えない。残る前提は 5b だけなので、Handoff 11 で `art-director` に 5b を始める。Handoff 11 は、受け手 `art-director` の Works from(設計仕様の視覚的含意、美術方針と制約)に合わせて Studio が組み立てた。Handoff 10 の Findings のうち視覚に関わる客観的な事実(怯まない 3 状態、接触の解決の仕方)だけを抜き出し、`game-designer` の Sender assessment と実装側への影響(Playtester・art に不要)は渡していない。`design/combat.md` §10 の本文はこの操作の入力になかったため、Handoff 11 では要約せず Load で指定した。Previous handoff を none にしたのは、Handoff 10 に Sender assessment が含まれ、5b の方針(渡さない)に反するため。
- 2b(欠陥 D の `qa`)の Handoff は今回も作っていない。理由: この操作で書けるのは seq 11 の 1 つで、5b の方が Build を止めている前提になる。2b は Build を止めず、独立している(Build の前に結果があれば、欠陥修正を Build に加える)。Owner の報告の原文が入力にないため、推測で書かない。
- Build の Handoff を作るときの条件(Route 手順 4–5 のため記録): 5b の結果(視覚要素の一覧、既存の仕組みで足りるかの見立て)と `design/combat.md`、D-004、D-005 を渡す。Handoff 10 の「実装側への影響」(解決済みフラグ、除外状態、遠い方の選択はデータの規則)は技術情報として `gameplay-engineer` に渡してよいが、Sender assessment は渡さない。
- 5b(Design)の後: 視覚仕様(Handoff 12、D-006)は `outcome: done`。`art-director` は戦闘の規則・数値の変更は不要と判断しており、`question` ではない。D-001〜D-005 の範囲内で、新ボタンも方向・スコープの変更もなく、エスカレーションの条件に当たらない。5b を `done` にし、計画どおり Build(6)を `open` にした(Handoff 13)。
- Handoff 13 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from(承認済みの仕様、計画、制約、リポジトリ)に合わせ、Handoff 12 の Findings から視覚要素と見立て・未確認の点を客観的な事実として抜き出した。Handoff 12 と同様、Sender assessment(確信度、費用の見立ての根拠)は渡していない。Handoff 08 も Previous handoff にせず(Sender assessment に欠陥 D の仮説があるため)、計画の内容は D-004 を Load で渡す。Handoff 12 は編集していない(`to: studio` で、Load は Studio の routing のため)。Expected output に、Verify で `qa` と `art-director` を並列にするための `to: studio` と、T0 の結果で前提が崩れたときの戻し先(仕様の欠落は Design、計画の不成立は Plan、視覚要素の実現不能は `art-director` への仕様調整を Studio 経由で)を書いた。
- 未処理(Build を止めない): Handoff 12 の Open question により、`design/combat.md` §10 に `design/grub-charge-telegraph.md` への参照を追記する必要がある。書き込めるのは `game-designer` のため、後続の Studio 操作で小さな Handoff(次の空き seq)として回す。Build は視覚仕様を Load で直接読むので、これを待たない。ただし Verify の前に済ませる。
- Playtester に渡す Handoff には、視覚仕様 §10.2 の体験の観点を書かない(Handoff 12 の指示、および Playtester の Independence)。
- 6(Build 1 回目)の後: Handoff 14 は `outcome: question`。実装に入らず、T0 を完了できなかった理由は、その実行にゲームのコード・ビルド・テスト実行の手段がなかったこと。`project.md` は `repository: none`(サンプルで、ビルドは `sim/` で模擬)と明記しており、Handoff 14 の選択肢 (a)「リポジトリを使える形で Build をやり直す」は Studio が用意できない。選択肢 (b)「別の担当に T0 だけをさせる」も、同じ入力では同じ結果になる。したがって Studio 単独で選べる process の問題ではなく、Build をどう進めるかという技術方針・順序(`technical-director` の権限)の問題になる。戻りルール「Build: 計画が成り立たない場合 → Plan(`technical-director`)」に従い、Plan(6a)を新設して `open` にした。Build(6b)は 6a の結果を待つ。Verify(7)は成果物がないため始めない(Handoff 14 の要請どおり、Verify の Handoff は組まない)。
- 6 の後のエスカレーション確認: 仕様の曖昧さや矛盾は報告されておらず(`game-designer` へ戻す理由はない)、D-001〜D-006 のどれも変更を要しない。コンセプト・柱・Decision の変更はなく、新ボタンもない。現時点では Owner のエスカレーションの条件に当たらない。ただし 6a で `technical-director` が「模擬環境では D-004 の前提を確かめる手段がなく、Build を成立させるには Owner の判断(リポジトリの提供、またはスコープ・リスクの受け入れ)が要る」と結論した場合は、スコープ・リスクの大幅な変化に当たりうるため、`technical-director` が `prepare-owner-escalation` で Escalation を作る。Handoff 15 の Expected output にそう書いた。
- Handoff 14 の Open questions 2(要素 9)と 3(必須視覚要素 1〜6 が既存の仕組みで実現できるか)は技術方針に関わるため、6a の Handoff 15 に含めた。Handoff 14 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Sender assessment は Handoff 15 に転記せず、客観的な事実(報告された `sim/repo-notes.md` の内容、確認できなかった項目)だけを Findings に抜き出した。無敵フラグの共有構造は欠陥 D の原因候補だが、確定していない仮説なので「`sim/repo-notes.md` に書かれた事実」としてのみ渡し、欠陥 D の原因とは結び付けていない。`technical-director` は `qa` ではないため、事実の伝達は問題ない。
- 2b の `qa` Handoff と `game-designer` の §10 追記 Handoff は、今回も作っていない(この操作で書けるのは seq 15 の 1 つで、Build の再開の前提である 6a を優先した)。どちらも 6a と独立で、残っている。
- 6a(Plan)の後: Handoff 16(D-007)は `outcome: done`。`technical-director` は D-004 の方針を保ち、T0 を「前提の台帳」(7 項目。各項目に置く前提・確認する場所・崩れたときの戻し先)に置き換え、接触結果の通知(視覚仕様の要素 9)を D-004 の口に足し、読めるコードが全くない場合は再試行せず返す条件(D-007 の 7)を定めた。仕様・方向の変更は不要で、`game-designer`・`game-director` に回す事項はない。D-001〜D-006 は変わらず、新ボタンもない。Owner の Escalation は `technical-director` が「今回は作らない」と判断した(作業が戻しやすい、D-004 の骨格は `sim/repo-notes.md` で確認済み、方針が変わりうる未確認項目は 2 点で実装の入口で見える)。Studio も、Escalation の条件に今は当たらないと確認した。6a を `done`、6b を `open` にした。
- 6a の後に残るリスク: Build が書き換えられるコード自体がない場合、計画は空になる。Handoff 17 の Expected output で、最初にコードを読み書きできるかを報告させ、できない場合は再試行せず `outcome: question` で返す(D-007 の 7)。その結果を受けた次の Route で、Escalation が要るかを `technical-director` に判断させる。Studio は先回りして Escalation を書かない。
- Handoff 17 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 16 の Findings から台帳、共通手順、接触結果の通知、視覚要素の段階、並列化、無敵の問い合わせ関数、テスト戦略、打ち切りの条件を客観的な内容として抜き出した。Handoff 16 の Sender assessment は渡していない。Previous handoff は none。無敵のタイマーについては、触れない・フラグを共有しているという事実と V3、V4 の測定条件のみを渡し、欠陥 D の原因とは結び付けていない。
- Handoff 17 の Expected output に、Verify で `qa` と `art-director` を並列にするため `to: studio` を指定した(Build の Sender assessment は `qa` に渡さない)。縮小案を使った場合は、Studio が `art-director` に受け入れ基準(A6、A7 など)の読み替えを確認する必要がある。
- 6b(Build 再開)の後: Handoff 18 は `outcome: question`。最初の確認の結果、実行環境にゲームのコード・ビルド・テスト手段・リポジトリがなく、変更を加える経路もなかった。台帳 7 項目はすべて未確認で、実装・テスト・ビルドノートはなく、`qa` / `art-director` に渡せる成果物もない。D-007 の 7 に該当するため、Build は再試行しない。Studio は、Build を同じ入力で再び開始しない(結果が変わらないため)。仕様の曖昧さや矛盾は報告されておらず、`game-designer` に回すものはない。D-001〜D-007 の変更も要しない。
- 6b の後の route 改訂: 6a で `technical-director` は「今回は Escalation を作らない」と判断したが、その前提(コードにアクセスできる可能性)は崩れた。リポジトリの提供、または Build の範囲を模擬に合わせて縮めることは、スコープ・費用・リスクが Goal の想定から大きく変わりうる(Escalation の条件)。ただし、要否と選択肢の設計は技術リスクの判断であり、`technical-director` の権限(Escalation の準備は `prepare-owner-escalation`)にあるため、Studio は先回りして Escalation を書かず、Plan(6c)を新設して `open` にした(Handoff 19)。Verify(7)は成果物がないため始めない。Play(8)と Review(9)は 6c の結果に依存するため `planned` のまま、範囲が変わりうると注記した。
- Handoff 19 の作り方(Route 手順 4–5): 受け手 `technical-director` の Works from に合わせ、Handoff 18 の Findings(確認できたこと・できなかったこと、選択肢 (a)(b)、再開順序)を客観的な事実として抜き出した。Handoff 18 の Sender assessment は転記していない。Previous handoff として Handoff 18 を Load に入れた(`technical-director` に Sender assessment を除外する方針はない)。Handoff 18 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Handoff 19 の Expected output は、Owner の判断が要る場合は Escalation(seq 20、`to: owner`)、不要な場合は `to: studio` の Handoff とした。
- 6c(Plan)の後: Escalation 20 で、`technical-director` は Owner の判断が要ると結論し、選択肢 A(実際のリポジトリとビルド・テスト手段の提供)、B(Build の範囲を実装計画と受け入れ基準の確定までに縮小)、C(模擬ビルドで工程を予行)と推奨(B。ただし実コードがあり実機で確かめたいなら A)を示した。Studio も、スコープ・費用・リスクが Goal の想定から大きく変わることを確認し、エスカレーションの条件に当たると判断した。6c を `done` にし、6d(Owner)を `open`、Goal を `blocked-on-owner` にした。
- Resume(Owner の回答、2026-10-10): Owner は Escalation 20 に Option C で回答し、条件を付けた(`sim/repo-notes.md` をコードとして扱う、Build は変更内容を Handoff に正確に書いた時点で完了、模擬ビルドはランタイムのシミュレーターが変更内容から作る、結果に模擬であることを明記し Goal の判定は模擬ビルドに基づく)。Studio は D-008(`decided_by: owner`)に Owner の言葉を含めて記録し、Escalation 20 を `resolved`(`decision: D-008`)にして、Goal を `active` に戻した。6d を `done` にした。
- Resume の route 再計画: Escalation の Option C の "If chosen" は「Owner が模擬ビルドの記述を提供した時点で Verify から再開、Goal は達成扱いにしない」だった。Owner の回答は、それとは異なる点が 3 つある。(1) 模擬ビルドを作るのは Owner ではなくランタイムのシミュレーターで、その元は Build の変更内容である。(2) `sim/repo-notes.md` をコードとして扱うため、Build(`gameplay-engineer`)は変更内容を書く工程として残る。(3) Goal の判定は模擬ビルドに基づいて行う。そのため、選択肢の記述どおりには進めず、Owner の言葉を優先して残りの route を再計画した(Resume 手順 3、選択肢に記述のない回答)。変更点は次のとおり。Build(6e)を新設して `open` にし、Handoff 21 を作った。Verify(7)、Play(8)、Review(9)は模擬ビルドを対象にし、Review は模擬ビルドに基づく判定にする。Goal を達成扱いにしない、という Escalation の記述は Owner の条件で置き換わった。ただし、結果には模擬であることを明記し、実機で確認できない点(H1〜H4)を Outcome に書く。
- 再計画での Escalation 確認: Owner の回答は D-001〜D-007、ビジョンの柱、入力ボタンに触れない。新しい Escalation の条件には当たらない。シミュレーターは Role ではないため、route の行には置かない。模擬ビルドの作成は 6e と 7 の間のランタイムの動作で、Next action に記す。
- D-007 の 7 の扱い: コードを読めない入力の欠落は、`sim/repo-notes.md` を Load に入れたことで解消した。Handoff 21 で、台帳 7 項目は `sim/repo-notes.md` に照らして確認し、答えがない項目は「模擬上の前提」と明記するよう指示した。実コードで確認済みと書かせない。
- Handoff 21 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、仕様と計画は Load で渡した。Previous handoff は Studio が書いた Handoff 17(Sender assessment がない)にした。Handoff 18 は Sender assessment を含むため Load に入れず、必要な事実は Handoff 21 に転記した。Expected output は `to: studio` として、Verify の `qa` と `art-director` への Handoff を Studio が組み直せるようにした。欠陥 D の原因の推測は書かせない。
- 2b の `qa` Handoff と `game-designer` の §10 追記 Handoff は、今回も作っていない(この操作で書けるのは seq 21 の 1 つ。どちらも Owner の回答に依存せず、Build とも独立で、残っている)。2b は Owner の報告の原文が入力にない限り作れない。§10 の追記は Verify の前までに済ませる。
- 6e(Build)の後: Handoff 22 は `outcome: question`。台帳 7 項目を `sim/repo-notes.md` に照らして確認し(1〜5 と 7 の一部は「模擬上の前提」と明記)、変更内容は 2.1〜2.4 に完全に書かれた。ただし波 2 以降の条件(K / T)をいつから調べ始めるか、出現位置の待ちの敵を「生きている敵」に数えるか、が仕様 §4.1 に未定義で、文面どおりだと部屋 2 の波 2 が即座に出うる(V7 に影響)。戻りルール「Build: 仕様の欠落 → Design(`game-designer`)、その後 Build に戻る」に従い、Design(6f)を新設して `open` にした。エンジニアは決めない(Skill どおり)。6e を `done` にした。
- 6e の後のエスカレーション確認: 欠落は波の出現条件の細部で、D-001〜D-008、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。`game-designer` の権限(規則、ルールの細部)内の決定で、Owner エスカレーションの条件に当たらない。`game-director` に回す必要もない。ただし `game-designer` の答えが D-002・D-003 の変更やスコープの変更を要する場合は、`question` で返して Decide(`game-director`)に回す(Handoff 23 に書いた)。
- 6f の Handoff(23)の作り方(Route 手順 4–5): 受け手 `game-designer` の Works from に合わせ、Handoff 22 の Findings の「5. 仕様の欠落」から、欠落の事実、部屋ごとの K・T、選択肢 A / B / C と技術的な費用だけを抜き出した。Handoff 22 の Sender assessment(確信度、疑い 1〜3)は渡していない。`gameplay-engineer` が提案した既定 A は、選択肢の説明として「提案されている」とだけ事実を伝え、決定は `game-designer` に委ねた。Previous handoff は none(Handoff 22 が Sender assessment を含み、大部分が受け手に不要なため)。Handoff 22 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- 小さな追記の統合: 以前から残っていた「`design/combat.md` §10 に視覚仕様への参照を追記する」作業は、書き込めるのが `game-designer` で、6f と同じファイルを触るため、Handoff 23 に含めた。Verify の前までに済ませる条件はこれで満たされる。
- 6f の後: 規則の決定は Decision(D-009 を `game-designer` が記録する想定)にする。6g で Studio が `gameplay-engineer` への小さな Handoff を組み、2.1 に 1 文だけ足して Build の記述を確定させ、`to: studio` で返す。その後、シミュレーターが模擬ビルドを作り、Verify(7)を組む。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 23 の 1 つで、Build の確定に必要な 6f を優先した)。Verify の前にある必要はないが、結果が欠陥修正を要するなら Build の再開が必要になるため、できるだけ早く処理する。
- 6f(Design)の後: Handoff 24(D-009)は `outcome: done`。`game-designer` は案 A(前の波の全員が出現中に入った時点から K・T を調べ始め、待ちの敵は生きている敵に数えない)を決め、`design/combat.md` の §4.1、§4.3 の注、V7、V12(新規)、§6.2、§8、§9 を更新し、§10 に視覚仕様への参照を追記した。数値・入力・プレイヤー側の値は変えていない。D-001〜D-003 の変更もスコープの変更もなく、`game-director` に回す必要はない。エスカレーションの条件(コンセプト・柱・Decision の変更、スコープ・費用・リスクの大幅な変化、Owner の好みが基準、不可逆、Goal の再解釈)のどれにも当たらない。6f を `done` にし、計画どおり 6g を `open` にした(Handoff 25)。§10 の参照追記は済んだので、Verify の前の条件は満たされた。
- Handoff 25 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 24 の Findings から規則と足す 1 文、足りない部分の確認点を客観的に転記した。Handoff 24 には Sender assessment がなく、Previous handoff として Load に入れた。Handoff 22 の Sender assessment は転記していない。Handoff 24 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、Verify の `qa` と `art-director` への Handoff を Studio が組み直せるよう、確定した変更内容の全体を Findings に自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。模擬上の前提が残る項目も一覧させる。
- Verify(7)の Handoff を作るときの条件(Route 手順 4–5 のため記録): `qa` には受け入れ基準(V7、V12 を含む)と模擬ビルドの動かし方のみを渡し、Build の Sender assessment は渡さない。`art-director` には視覚仕様と模擬ビルドを渡す。Playtester(8)には模擬ビルドとプレイヤー像のみで、仕様の数値や体験の観点(§6.2、視覚仕様 §10.2)は書かない。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 25 の 1 つ)。独立で、残っている。
- 6g(Build)の後: Handoff 26 は `outcome: question`。止まった原因は入力の欠落だけである。Handoff 25 の Load に Handoff 22(変更内容の記述 2.1〜2.4)が入っておらず、`gameplay-engineer` は記述の全体を推測せずに返した。これは Studio の Load の漏れで、仕様の曖昧さや矛盾は報告されていない(`game-designer` に回すものはない)。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-director` に回す必要もない。Handoff 26 の選択肢 (a)(Handoff 22 などを Load に入れて同じ Step をやり直す)を採った。選択肢 (b)(Handoff 22 抜きで書き直す)は、記述の食い違いを保証できないため採らない。6g を `done` にし、6h を `open` にした(Handoff 27)。ループ制限には当たらない(初めての欠落で、受け入れ基準の失敗でもない)。ただし Handoff 27 でも必須ファイルが読めない場合は、再試行せず返すよう指示した。その場合は次の Route で、パケットの組み方そのものを見直す。
- Handoff 27 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせて組んだ。Load に Handoff 22(記述の元)、Handoff 17(台帳。Handoff 16 は `technical-director` の Sender assessment を含むため使わない)、設計書 2 点、`sim/repo-notes.md`、D-004〜D-009 を加えた。Previous handoff は Handoff 26 にした(`gameplay-engineer` 自身が書いたもので、Sender assessment を除外する方針は `gameplay-engineer` にない)。Handoff 22 の内容は、この操作の入力になかったため要約せず、Load での指定に留めた。Handoff 26 の Findings 2〜4 は「下書き」として渡し、Handoff 22 と台帳に照らして確認させ、食い違いは Handoff 22 側を正とするよう書いた。Handoff 26 は編集していない(`to: studio` で、Load は Studio の routing のため)。
- Handoff 26 が V12(b) について指摘した帰結(待ちの間に R の Grub を倒していたら、波 2 はすぐ出る)は、Verify の Handoff を組むときに期待値として渡す必要がある。Handoff 27 に記録した。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 27 の 1 つ)。独立で、残っている。
- 6h(Build)の後: Handoff 28 は `outcome: done`。変更内容 2.1〜2.4 に D-009 の 1 文が統合され、Handoff 22 を読まなくても分かる形で確定した。Handoff 22 と D-009 の間に、1 文の統合以外の食い違いはなく、`game-designer` に回す問いもない(§4.3 の表の注記の言い回しが紛らわしいという指摘は、規則の食い違いではなく、表現の整理の提案として残る。Verify の期待値には影響しない)。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-director` に回す必要もない。6h を `done` にし、計画どおり Verify に進む。
- Verify の route 改訂: Verify(7)を 7a(`qa`)と 7b(`art-director`)の並列に分けた。7a と 7b は互いの出力を使わない。この操作で書けるのは seq 29 の 1 つだけなので、`qa` の Handoff(29)を先に作り、7b の Handoff は後続の Studio 操作が次の空き seq で作る。Play(8)は 7a と 7b の両方の後。
- 模擬ビルドの扱い: 模擬ビルドは、プロジェクトのファイル一覧に `sim/build-0.4.md` として存在する。Handoff 28 の変更内容からシミュレーターが作ったものとして扱い、Handoff 29 の Load に指定した。この操作の入力に `sim/build-0.4.md` の中身はなく、内容を確認していない。`qa` が読めない、または記述と矛盾する場合は、`qa` は推測せず報告する。
- Handoff 29 の作り方(Route 手順 4–5): 受け手 `qa` の Works from(受け入れ基準、変更の動かし方、制約。実装者の自己評価や説明は渡さない)と Independence に合わせ、Studio が新しく組んだ。Handoff 28 は Sender assessment を含み、かつ実装の説明なので Previous handoff にも Load にも入れていない(Previous handoff は none)。受け入れ基準は `design/combat.md` の V1〜V12 を Load で指定し、本文は要約しなかった。V12 の期待値「待ちの間に先に出ていた敵を倒すと、次の波はすぐ出る」は、仕様(§4.1、D-009)の規則から導かれる期待値として、実装の説明を添えずに書いた。Handoff 28 は編集していない(受け手は Studio で、Load は Studio の routing のため)。欠陥 D の原因の推測は渡していない。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 29 の 1 つ)。独立で、残っている。Play の前までに処理する必要はないが、欠陥の修正が要る場合は Build の再開が必要になる。
- 7a(Verify)の後: Handoff 30 は `outcome: question`。V1〜V12 に fail はなく、同じ基準が 2 回失敗した事例もないため、Verify の戻りルール(2 回目の失敗は Plan)は発動しない。V7(Grub の速度の数値、遠い角が同距離のときの規則)と V10(プレイヤー側の数値)は、模擬ビルドの記述に書かれておらず、pass にできない。さらに基準外で、仕様 §3.3 と模擬ビルドの食い違い F-1(突進の再開始の待ち時間の起点が、仕様は Recovery 終了後、ビルドは突進終了後)が見つかった。
- 7a の後の route 改訂: (a) F-1 は「ビルドされた挙動が仕様と違う」ので、戻りルール「Verify: fail(built behavior differs)→ Build(`gameplay-engineer`)」に従い、Build(7c)を新設して `open` にした(Handoff 31)。仕様の文面が曖昧なら、`gameplay-engineer` は直さずに `game-designer` への質問として返す(Handoff 31 の Open questions 1)。Studio は意図を決めない(`game-designer` と `qa` の権限)。(b) V7 と V10 の未確認は、模擬ビルドの記述の欠落であり、元は変更内容(Handoff 28 の 2.1〜2.4)に数値と規則が書かれているかの問題になる。速度は仕様に数値があり、遠い角が同距離のときの規則と、プレイヤー側の数値が「変えていない」と明記されていないことが原因と見て、同じ Build(7c)で変更内容に明記させる。仕様に規則がない場合は `outcome: question` で返し、次の Route で `game-designer` に回す。(c) 再検証 7d(`qa`)を 7c の後に `planned` で加えた。(d) 7b(視覚)は F-1 の修正に影響されないので、7c と並行して作れる。次の空き seq で Handoff を組む。
- 7a の後のエスカレーション確認: F-1、V7、V10 の扱いは、D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。コンセプト・柱・Decision の変更はなく、スコープ・費用・リスクの大幅な変化でもなく、不可逆でもない。Owner のエスカレーションの条件に当たらない。`game-director` に回す必要もない。
- 欠陥 D の扱い: Handoff 30 が、模擬ビルド 0.4 は被弾直後のダッシュ中にダメージを受けうることを記述しており、仕様は意図的に未定義で、Play の「抜けた」という感覚(§6.2)に影響しうると報告した。規則を決めるのは `game-designer` だが、Director の指示(2b の再現結果が出てから規則を書く)は変えない。Owner の元の報告文が入力にないため 2b の Handoff は今回も作れない。Play の前に扱うかどうかは未決なので、Design(7e)を `tentative` で加えた(条件は route 表に記載)。この操作で書けるのは seq 31 の 1 つだけで、Build の修正(7c)を優先した。Handoff 31 には欠陥 D の原因の推測や規則の変更を書かず、範囲外と明記した。
- Handoff 31 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 30 の Findings(`qa` の報告。Sender assessment を持たない)から F-1、V7 の未確認 2 点、V10 の未確認、補足(V12(c))を客観的な事実として転記した。`qa` の Independence は受け手が `qa` の場合の制約で、`gameplay-engineer` への制限ではないため、Handoff 30 を Previous handoff にした。修正する変更内容の元は自分が書いた Handoff 28 で、Load に入れた(Handoff 26 の漏れの再発防止)。Handoff 30 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、再検証 7d の `qa` Handoff を Studio が Sender assessment を除いて組み直せるよう、修正後の変更内容の全体を Findings に自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。
- ループ制限の確認: 同じ受け入れ基準が 2 回失敗した事例はない。7c の後の再検証で F-1 または V7・V10 が再び落ちた場合は、`technical-director` に回す。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 31 の 1 つ)。独立で、残っている。
- 7c(Build)の後: Handoff 32 は `outcome: done`。修正後の変更内容 2.1〜2.4 の全体が自己完結で書かれ、`question` ではない。仕様の欠落・矛盾の報告はなく、`game-designer` に回すものはない。F-1 は仕様 §3.3 の文面が曖昧ではなく、仕様に合わせて起点を「Recovery の終了」と明記した。V7(Grub 速度 2.0 / 2.0 / 2.2 / 2.2 / 2.4、遠い角が同距離なら FL)と V10(プレイヤー側の数値は変更なし)も明記され、V12(c)の1文も足された。数値・規則・入力は変わらず、D-001〜D-009、ビジョンの柱、スコープに触れない。エスカレーションの条件に当たらず、`game-director` に回す必要もない。7c を `done` にし、計画どおり再検証 7d を `open` にした(Handoff 33)。
- 7c の後の注意点: Handoff 32 の報告によれば、Handoff 28 の変更内容は、すでに F-1 の起点を「前回の Recovery が終わってから」と書いていた。つまり、模擬ビルド 0.4 が「突進が終わってから」と書いた原因は、変更内容の曖昧さではなく、シミュレーターが記述を写す過程にある可能性がある(推測であり、確定していない)。7d で、更新された模擬ビルド(`sim/build-0.5.md`)がまだ F-1 を食い違いとして示すなら、それは同じ基準の2回目の食い違いとして扱い、ループ制限(同じ受け入れ基準が2回 fail → `technical-director` に回す)に従う。Studio は原因を決めつけない。
- Handoff 33 の作り方(Route 手順 4–5): 受け手 `qa` の Works from(受け入れ基準、変更の動かし方、制約。実装者の自己評価と説明は渡さない)と Independence に合わせ、Studio が新しく組んだ。Handoff 32 は変更内容の説明と Sender assessment を含むため、Previous handoff にも Load にも入れていない。期待値(F-1 の起点、V7 の数値と同距離の規則、V10、V12(c))は、仕様 `design/combat.md` と D-005、D-009 から導かれる内容として書き、実装の説明は添えていない。Previous handoff は Handoff 30(`qa` 自身の前回の報告で、Sender assessment を持たない)にした。欠陥 D は範囲外とし、原因の推測は渡していない。結果は `to: studio` にした(Play の Handoff を Studio が実装の履歴なしで組むため)。Handoff 32 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- 模擬ビルドの扱い: `sim/build-0.5.md` は、Handoff 32 の変更内容からシミュレーターが作ったものとして扱う。この操作の入力に中身はなく、Studio は内容を確認していない。
- 7b と 2b の Handoff は、今回も作っていない(この操作で書けるのは seq 33 の 1 つ。7b は 7d と独立で、Play の前までに作る。2b は Owner の報告の原文が入力にないため作れない)。
- 7d(Verify)の後: Handoff 34 は `outcome: question`。fail はない。F-1、V10、V12(c) は解消し、V1〜V12 の回帰も pass(模擬)。残った 1 点は V7 の「同距離のとき」の規則の用語で、ビルド 0.5 は「front-left corner」と書き、他の箇所の far-left / far-right と食い違うため、仕様の FL(奥の左隅)を指すか `qa` が確認できなかった。F-1 は前回と同じ点だが今回は食い違わず、V7 は前回は「記述なし(未確認)」、今回は「用語が曖昧(未確認)」で、どちらも fail ではない。したがって「同じ基準が 2 回 fail」のループ制限は発動しない。
- 7d の後の route 改訂: 期待値は仕様と D-005 で定義済みで(`qa` も明言)、Design(`game-designer`)に回す問いはない。問題は変更内容の記述の用語に限られるため、戻りルール「Verify: 食い違い → Build(`gameplay-engineer`)」に従い、Build(7f)を新設して `open` にした(Handoff 35)。再確認 7g(`qa`)を 7f の後に `planned` で加えた(同距離の規則だけ。他の基準が変わっていないことを確認する。F-1、V10、V12(c) は再確認不要)。Play(8)の前提を 7b、7g(必要なら 7e)に直した。`qa` の確認方法の候補(ビルド記述の修正、または等距離の位置での開発用ログ確認)のうち、模擬では実機の位置確認が使えず、記述の修正が最小で足りるため、前者を採った。
- 7d の後のエスカレーション確認: 用語の明記だけで、D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。エスカレーションの条件に当たらず、`game-director` にも回さない。
- 注意(ループ制限): 7f の後の 7g で、V7 の同距離の規則が再び確認できない、または仕様と違う場合は、V7 の同じ基準が連続して通らないことになる。その場合は `technical-director` に回し、記述→シミュレーター変換の経路そのものを見直させる。Handoff 35 の Open question 1 で、Handoff 32 の記述が FL と書いていたかを事実として報告させる。FL と書いていたなら、用語のずれはシミュレーター側の可能性があるが、Studio は原因を決めつけない。
- Handoff 35 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 34 の Findings(`qa` の報告。Sender assessment を持たない)から、V7 の同距離の規則に関する客観的な事実だけを転記した。Previous handoff は Handoff 34、修正前の変更内容の元は Handoff 32(自分が書いたもの)を Load に明記した(Handoff 26 の漏れの再発防止)。`sim/build-0.5.md` は参照のみ。Handoff 34 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、7g の `qa` Handoff を Studio が Sender assessment を除いて組み直せるよう、修正後の変更内容の全体を自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。
- 7b と 2b の Handoff は、今回も作っていない(この操作で書けるのは seq 35 の 1 つ。7f が 7g と Play への経路を止めているため優先した。7b は 7f と独立で、次の空き seq で作れる。2b は Owner の報告の原文が入力にないため作れない)。7b は更新される模擬ビルドを使うため、7f の後に作る方が再作業を避けられるが、7f と並行して作ってもよい。
- 7f(Build)の後: Handoff 36 は `outcome: done`。修正後の変更内容 2.1〜2.4 の全体が自己完結で書かれ、`question` ではない。Handoff 32 は同距離の規則を「FL を選ぶ」と書いており、「front-left」「手前の角」の語はなかったと報告された。つまりビルド 0.5 の「front-left corner」はシミュレーターが記述を写す過程で生じた可能性があるが、推測であり、Studio は原因を決めつけない。今回の記述は FL = 奥の左隅(far-left corner)の対応表を足し、同距離は FL、手前の角のスロットは存在しないと明記した。数値・規則・入力は変わらず、仕様の欠落・矛盾の報告もない。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンに触れず、エスカレーションの条件に当たらない。`game-designer`・`game-director` に回す必要もない。7f を `done` にし、計画どおり 7g を `open` にした(Handoff 37)。
- Handoff 37 の作り方(Route 手順 4–5): 受け手 `qa` の Works from(受け入れ基準、変更の動かし方、制約。実装者の自己評価や説明は渡さない)と Independence に合わせ、Studio が新しく組んだ。Handoff 36 は変更内容の説明と Sender assessment を含むため、Previous handoff にも Load にも入れていない。期待値(同距離は FL = 奥の左隅、手前の角のスロットは存在しない、選び直さない)は、仕様 §4.1 と D-005 から導かれる内容として書き、実装の説明は添えていない。「何を直したか」も伝えていない。Previous handoff は Handoff 34(`qa` 自身の前回の報告)。模擬ビルドは `sim/build-0.6.md`(Handoff 36 の変更内容からシミュレーターが作ったものとして扱う。この操作の入力に中身はなく、Studio は内容を確認していない)。結果は `to: studio`。Handoff 36 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- ループ制限の確認: 7g で V7 の同距離の規則が再び確認できない、または仕様と違うと報告された場合は、同じ基準が連続して通らないことになる。その場合は `technical-director` に回し、記述→模擬ビルド変換の経路を見直させる。
- 7b と 2b の Handoff は、今回も作っていない(この操作で書けるのは seq 37 の 1 つ。7b は 7g と独立で、Play の前までに作る。最新の模擬ビルドは `sim/build-0.6.md`。2b は Owner の報告の原文が入力にないため作れない)。
- 7g(Verify)の後: Handoff 38 は `outcome: pass`。V7 の同距離の規則は、ビルド 0.6 の記述で「the far-left corner」と書かれ、手前の角は「there is none」と明記されており、仕様の FL(奥の左隅)以外を指せない。部屋 3・4・5 の記述も同じ語で揃っている。V1〜V12 に fail も確認不能もなく、F-1、V10、V12(c) も前回から食い違っていない。すべて模擬ビルドの記述に基づく。V7 の同じ基準が連続して通らない事態にはならなかったので、ループ制限(`technical-director` への回付)は発動しない。7g を `done` にした。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-designer`・`game-director` に回すものもない。
- 7e(欠陥 D)の決定: `skipped` にした。理由: (a) 規則を決める権限は `game-designer` にあり、Director の指示(2b の再現結果が出てから規則を書く)がある。Owner の元の報告文が入力になく 2b を作れないため、Play の前に規則を決める根拠が揃わない。(b) 欠陥 D の挙動は模擬ビルドが記述しており、Playtester は何も知らされずに体験できる。Playtester に既知の欠陥として伝えると Independence に反し、観察を歪めるため、伝えない。(c) Play の結果が欠陥 D を体験の阻害要因と示した場合は、戻りルール(Play: 欠陥 → Observe(`qa`)、設計・体験の問題 → Diagnose(`game-designer`))に従い、その時点で再び回す。これは Studio の process 上の判断で、ゲームの内容は決めていない。Review では、欠陥 D を未再現の既知の疑いとして次の課題に挙げる。
- Handoff 38 は Previous handoff が 37 の `qa` 自身の報告で、受け手は Studio のため編集していない。また 38 の Open questions 2(実機でしか確認できない点: V3 の窓の端、30/60 FPS の実測、等距離のログ確認)は、Outcome の「実機で確認できない点」に H1〜H4 とあわせて書く。
- 7b の Handoff(39)を作った。Verify の残りは 7b だけで、Play の前までに必要なので、これを優先した。7b と 7g は互いの出力を使わず、7g が済んだ今、7b の入力(視覚仕様、D-006、美術方針、最新の模擬ビルド `sim/build-0.6.md`)は揃っている。Handoff 39 の作り方(Route 手順 4–5): 受け手 `art-director` の Works from(視覚的含意のある仕様、構築物のレビュー、美術方針と制約)に合わせ、Studio が新しく組んだ。実装の説明や Build の Sender assessment は渡していない。`qa` の報告から渡したのは、ビルド 0.6 に新しい音・新しいボタンがなく、点滅が 1 秒間に 3 回を超えないという客観的な事実だけにした。視覚仕様の本文は要約せず Load で指定した。Previous handoff は none。結果は `to: studio`(Play の Handoff を実装の履歴なしで組むため)。判定は模擬ビルドの記述に基づくことと、実機要の点を分けて書くことを指示した。Handoff 38 は編集していない。
- 模擬ビルドの扱い: `sim/build-0.6.md` の中身は、この操作の入力に Handoff 38 での引用の範囲でしかなく、Studio は全体を確認していない。`art-director` が読めない、または記述と矛盾する場合は推測せず報告する。
- 2b(`qa`、欠陥 D の再現)の Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 39 の 1 つ)。独立で、Play の前提ではなくなった(7e skipped)。原文を Owner から得られた時点で、次の空き seq で作る。
- 7b(Verify、視覚)の後: Handoff 40 は `outcome: pass`(模擬ビルド 0.6 の記述に基づく)。A1〜A13 に fail はない。A5 は確認不能(実機要)、A8・A9・A10・A11 には記述の欠落か実機要の部分が残る(欠落 G1〜G5 は矛盾ではなく、ビルドの修正は求められていない)。赤橙は害になる状態だけに使われ、D-006 に反しない。戦闘の規則・数値・入力の変更は不要で、新しい Decision(D-010)も作られていない。D-001〜D-009、ビジョンの柱、スコープに触れず、エスカレーションの条件に当たらない。`game-designer`・`game-director` に回すものもない。7b を `done` にし、計画どおり Play(8)を `open` にした(Handoff 41)。Verify の戻りルール(2 回目の失敗は Plan)に関わる事例はない。
- Handoff 41 の作り方(Route 手順 4–5): 受け手 `playtester` の Works from と Independence に合わせ、Studio が新しく組んだ。渡したのは、ビルドの入手(`sim/build-0.6.md`)、プレイヤー像(`project.md#player-profile`)、一般的な注意の向け先「戦闘」だけである。何が変わったか、期待する結果、受け入れ基準(V 系、A 系)、仕様の数値、欠陥 D の存在、Handoff 40 の内容は渡していない。Previous handoff は none、Decisions は none、Load は最小にした。結果は `to: studio`(Review の Handoff を Studio が組むため)で、判定や解決策の決定は求めず、読みだけでは判断できなかった点は「確認できなかった」と書くよう指示した。
- 指示と実際の差(Handoff 40 の Expected output 2): Handoff 40 は、§1.5 の実機項目と S1〜S3 を観察の観点として Play の Handoff に渡すよう求めていた。例の文言(「抜けたと感じたか」「レーンの上に立ったとき、まだ危ないと感じたか」など)は、設計側の仮説を示唆し、Playtester の Independence(期待する結果を示さない)に反するため、渡さなかった。Playtester は自由に観察を報告する。S1〜S3 と実機項目は、Play の報告が出た後に、Studio が観察報告と突き合わせる材料として下に残す。Playtester に渡さなかったことは Role の権限の変更ではなく、Studio の process 上の判断である。
- Play の後の戻し方(Handoff 40 の Expected output 3 と戻りルールを引き継ぐ): 「0.7 s では足りない」が出て、見た目の強調で補えないなら `game-designer` へ(`design/combat.md` §7)。S1(抜けた合図と出現中の輪の混同)、S2(解決後もレーンが赤橙のままの誤読)、Recovery の誤読が出たら `art-director` へ戻し、Handoff 40 の修正方針で見た目だけを直す(規則は変えない)。欠陥 D が体験の阻害要因と示された場合は、7e/2b の扱いに従う。
- 保留項目の引き継ぎ(Review 用): Handoff 40 の実機要項目(暗い床での 35% のレーン、レーンと弾・ランタイムの光の区別、0.7 s の十分さ、Recovery の誤読、かすりの感触、抜けた合図の過剰、小さい画面での尾根、30/60 FPS、色覚の差)、S1〜S3、ビルド記述の欠落 G1〜G5 は、Outcome の「実機で確認できない点」に H1〜H4、Handoff 38 の実機要の点(V3 の窓の端、30/60 FPS の実測、等距離でのログ確認)とあわせて書く。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 41 の 1 つ)。独立で、残っている。
- 8(Play)の後: Handoff 42 は `outcome: done`。Playtester は実機ではなく、`sim/build-0.6.md` の記述を読んで思い描いた体験を報告し、実時間・見え方・操作感・音・FPS 差は確認できなかったと明記した。報告に含まれる問題は A〜F(Findings は Handoff 43 に転記)で、Play の戻りルールに照らすと次のとおり。(a) 見た目の混同(S1、S2、Recovery の誤読)の報告はなく、`art-director` へ戻す理由はない。(b) 「0.7 s では足りない」の報告もなく、`game-designer` へ戻す理由もない(Playtester は 0.7 秒の長短を確認できなかったと書いている)。(c) 欠陥 D(問題 E)は、ビルド記述にある既知の挙動を観察として記したもので、「実際に起きるかは確認できなかった」。体験の阻害要因と示されたわけではないため、7e/2b の戻し条件は発動しない(2b は Owner の原文待ちのまま)。(d) 問題 A、B、F は設計・体験に関わるが、これらが Goal の意図を満たさないほどの問題か、D-002 の範囲で許容される帰結かは、Review の判断(`game-director` の権限)である。戻りルール「Play: 設計・体験の問題 → Diagnose」を先に適用すると、Review の判定の前に Diagnose を始めることになり、Goal の成否の判断を飛ばす。計画どおり Review(9)へ進み、Review の結果が `goal-not-met` なら戻りルール「Review: goal not met → Diagnose」に従う、とした。
- 8 の後のエスカレーション確認: Playtester の報告は D-001〜D-009、ビジョンの柱、スコープ、入力ボタンに触れない。コンセプト・柱・Decision の変更はなく、スコープ・費用・リスクの大幅な変化でも、Owner の好みが主な基準でも、不可逆でもない。Owner のエスカレーションの条件に当たらない。Review が方向の選択を伴うと判断した場合は、`game-director` が判断するか、条件に当たるなら Escalation を準備する(Handoff 43 の Expected output に書いた)。
- Handoff 43 の作り方(Route 手順 4–5): 受け手 `game-director` の Works from(診断、Review の入力としての Playtest 観察と QA 結果、ビジョン・制約・Decision)に合わせ、Studio が組んだ。Handoff 42(Playtester の報告。Sender assessment を持たない)の Findings を問題 A〜F の表、よかった点、仮説、疑問に分けて客観的に転記し、「模擬ビルドの記述を読んで思い描いた体験」であるという限界を最初に置いた。仮説は観察と分けて渡した。Previous handoff は Handoff 42。Handoff 38(`qa` の pass)と Handoff 40(`art-director` の pass)は Load の Project に置いた。`game-director` には Sender assessment を除外する方針はないが、いずれも `to: studio` の報告で、Sender assessment を持たない。Handoff 42 は編集していない(受け手は Studio で、Load は Studio の routing のため)。判定の基準(Goal の Interpretation)と、模擬ビルドに基づく判定にする条件(D-008)は、Findings と Constraints に書いた。Studio は判定を先取りしていない。
- 保留項目の突き合わせ(Play の報告との照合): S1〜S3 は Playtester の報告に現れていない(未確認)。Handoff 40 の実機要項目も、Playtester は確認できなかった項目に含めていない。Review の Outcome の「実機で確認できない点」に、前の Route 変更で記録した保留項目のすべてをそのまま残す。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 43 の 1 つ)。独立で、残っている。Review が欠陥 D を次の課題に挙げた場合、その後の新しい Goal として扱う。

## Next action

Goal は `active`。Review(9、`game-director`)が `open`。Handoff: `goals/G-001-combat-monotony/43-studio-to-game-director.md`。

1. `game-director` が Handoff 43 に従い、模擬ビルド 0.6 に基づいて、Goal の意図が満たされたかを判定し(`review-outcome`)、`to: studio` の Handoff(`44-game-director-to-studio.md`、`outcome: goal-met` または `goal-not-met`)で返す。方向の選択を伴う判断は Decision(D-010)にする。Owner の判断が要る場合は、決めずに Escalation を準備する。
2. 報告を受けた次の Route で、(a) `goal-met` なら Close(Outcome を `owner_language`(日本語)で書く。結果、Decisions、次の課題(欠陥 D の再現、部屋 1・3 の変化、張り付き戦法など)、Owner の項目、実機で確認できない点を含め、判定が模擬ビルドに基づくことを明記する)、(b) `goal-not-met` なら戻りルール(Review: goal not met → Diagnose、Review の findings を渡す)に従い `game-designer` に回す。ループ制限(Goal が Diagnose に 2 回入って進展がない場合は `game-director` が見直す)の確認も行う。
3. 2b(`qa`、`reproduce-defect`)は Owner の元の報告文が必要で、原文が入力にある場合に作る。Review が次の課題として欠陥 D を挙げた場合は、新しい Goal の提案として扱う。

Owner への報告(日本語):
- Playtester の観察報告が届きました。ただし、実機のプレイではなく、模擬ビルド 0.6 の記述を読んで思い描いた体験の報告で、実時間の感触、見え方、ゲームパッドの操作感は確認できていません。
- よかった点は、突進の予告で見てから避けられること、既存の操作だけで対応できること、隅でのスワイプだけの戦い方が部屋 2・4・5 で通用しないことです。気になる点は、部屋 1・3 に変化がないこと、突進 Grub に張り付く・離れすぎると突進を見ずに済む可能性、部屋 5 の突進の順序が読めないこと、欠陥 D(被弾直後のダッシュ中のダメージ。実際に起きるかは未確認)です。
- 見た目の混同や予告時間の不足は報告されなかったため、戻しは不要と判断しました。次に、`game-director` が模擬ビルドに基づいて Goal の判定(Review)を行います。Owner の判断は、今は不要です。
- 欠陥 D の再現(`qa`)には、Owner の元の報告文が必要です。原文をいただければ、いつでも回せます。

## Outcome

(未完了)
>>>END

<<<FILE goals/G-001-combat-monotony/38-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 38
from: qa
to: studio
stage: Verify
outcome: pass
---
# 38: qa → studio — 模擬ビルド 0.6 の再確認結果(V7 の同距離の規則は FL と確認、V1〜V12 は pass)

## Task

`sim/build-0.6.md` について、V7 の「同距離のときは FL」の規則を再確認し、V1〜V12 の記述が前回から崩れていないか確認した結果を報告する。Studio は、これをもとに Play(`playtester`)の Handoff を、実装の履歴を含まない形で組んでほしい。

## Context

G-001、Verify。**この報告はすべて「模擬ビルドの記述に基づく」(D-008)。実機で観測した証拠ではない。** 判定は `design/combat.md`(V7、§4.1、§4.3)、D-005、D-009 とビルドの記述だけから行った。実装側の説明や自己評価は使っていない。前回は Handoff 34(ビルド 0.5)で、V7 の同距離の規則だけが、記述の用語(「front-left」)のために確認不能だった。

## Findings

### 総合判定

- **pass(模擬)**。fail の基準も、確認不能の基準もない。
- V7 の同距離の規則は、FL(奥の左隅)を指すと一意に読める。前回の「front-left」という語は、ビルド 0.6 には残っていない。
- F-1、V10、V12(c) は前回 pass で再確認不要。ただし記述が前回と食い違っていないかは、読んだ範囲で見た。食い違いはなかった。

### 1. V7 の同距離の規則: pass(模擬)

期待値(仕様 §4.1 と D-005): 出現を決める時点のプレイヤー位置から、中心間の距離で FL と FR を比べて遠い方を選ぶ。同距離は FL。選択肢は奥の左隅と奥の右隅だけ。待ちの間は選び直さない。

ビルドの記述(原文):

- 「The farther-corner choice (rooms 3 and 5, wave 2) is made when the wave is triggered, before any waiting, using where you stand at that moment. The far-left corner and the far-right corner are compared by distance from the center of you to the center of each spot, and the one with the greater distance gets the Spitter. If the two distances are exactly equal, the far-left corner is used. It is never a near corner, because there is none. If you move while the wave waits, the choice does not change. A corner that a room names for a specific enemy is not part of this choice.」
- 「Each room has six spots where enemies appear: the door side, the far side (back middle), the left side, the right side, the far-left corner and the far-right corner. There is no spot in a near corner by the door. The only corners enemies appear in are the two far corners.」
- 「What play feels like now」の項: 「if you stand exactly equally far from both, it appears in the far-left corner.」
- 「Development build only」の項: 「For the farther-corner choice, the log shows which corner was chosen: far-left or far-right.」
- 「Timing at 30 and 60 FPS」の項: 「The farther-corner choice gives the same result at 30 and 60 FPS for the same positions.」
- 部屋 3 の記述: 「whichever far corner (far-left or far-right) is farther from you at the moment the wave is triggered」。部屋 5 は「chosen as in room 3」。

根拠:

- 同距離のときの角は、「the far-left corner」と書かれている。手前の角を指す語は、ビルド全体に出てこない。
- 手前の角については「there is none」と明記されている。このため、同距離の規則は奥の左隅(仕様の FL)以外を指せない。
- 部屋 4 の「Spitter in the far-left corner」と部屋 3・5 の「far-left or far-right」も同じ語で書かれていて、記述内に食い違いはない。
- 比べる距離(中心間)、選ぶ時点(波を出す時点、待つ前)、待ちの間に選び直さないこと、固定指定の角が対象外であること、の 4 点は、すべて仕様と一致する。
- 開発用ログに選ばれた角が出るので、実機では、等距離の位置で波を出してログを見れば確かめられる。この確認は、今回はしていない(模擬ビルドの記述を読んだだけ)。

### 2. V7 のその他の部分: pass(模擬)

- Grub 速度: 部屋 1〜5 が 2.0 / 2.0 / 2.2 / 2.2 / 2.4。ビルドは「Ordinary and charging Grubs in the same room walk at the same speed」「A charge always runs at 8.0」。仕様の表と一致する。
- 構成、K、T、Spitter 間隔は、§4.3 の表と一致する。
  - 部屋 1: 波 1 は通常 Grub(左、右)、波 2 は通常 Grub(奥)。1 体以下か 10 s。Spitter なし。
  - 部屋 2: 波 1 は突進型(奥)、波 2 は通常 Grub(左、右)+ 突進型(奥)。0 体か 15 s。
  - 部屋 3: 波 1 は Spitter(奥)+ 通常 Grub(左)、波 2 は Spitter(遠い角)+ 通常 Grub(右)。1 体以下か 12 s。間隔 2.0 s。
  - 部屋 4: 波 1 は Spitter(FL)+ 突進型(奥)+ 通常 Grub(左)、波 2 は Spitter(FR)+ 突進型(右)。1 体以下か 12 s。間隔 1.8 s。
  - 部屋 5: 波 1 は Spitter(奥)+ 通常 Grub(左、右)、波 2 は Spitter(遠い角)+ 突進型(左、右)。1 体以下か 12 s。間隔 1.6 s。
- 合計と同時最大数: 3/2、4/3、4/3、5/3、6/4。仕様と一致する。
- 「T s」の起点と「生きている敵」:
  - 「The timer starts when the last enemy of the earlier wave has finished fading in. If that enemy had to wait at its spot first, the timer starts after the wait and the fade-in.」
  - 「Enemies that are fading in count as living. Enemies still waiting to appear do not count.」
  - 「the next wave's threshold and timer are not running. They start only once every enemy in the wave has begun fading in.」
  - いずれも §4.1 と D-009 に一致する。

### 3. V1〜V12(ビルドの記述の範囲)

| 基準 | 結果 | 根拠(ビルド記述) |
|---|---|---|
| V1 | pass(模擬) | 「Wind-up, 0.7 s」→ Charge → 「Recovery, 0.8 s」の順。開始条件に「at least 1.5 s have passed since it finished fading in」。「Pausing freezes all timers and animations」「Resuming after a long pause does not skip ahead more than a short step (0.05 s)」。30/60 FPS の差は約 0.034 s 以内。 |
| V2 | pass(模擬) | 「rushes along the lane at 8.0 for up to 7 tiles (about 0.875 s), or until it hits a wall」。「The direction is fixed; moving afterwards does not turn the lane.」 |
| V3 | pass(模擬)。窓の端の数値は未測定 | 「The first time the Grub's body overlaps you during a charge decides it.」「the dash ending while it still overlaps you, does not hurt you.」「At 30 FPS the end of the dash's 0.25 s protection can differ from 60 FPS by up to one frame (about 0.034 s).」窓の端の数値(0.05 s 外れると被弾)の記述はない。実機で測る必要がある。直前 0.8 s 以内の被弾は対象外(欠陥 D)。 |
| V4 | pass(模擬) | 「A charge can hurt you at most once.」「If it was already overlapping you as the charge began, that counts as the first moment.」「Overlap during the wind-up or recovery does nothing. A new charge starts the count again.」無敵なら通り抜け、その後も当たらない。 |
| V5 | pass(模擬) | 「no other living charging Grub is currently winding up or charging」。「A dying winder or charger removes its lane within 0.1 s, and another charging Grub may then start its own wind-up.」 |
| V6 | pass(模擬) | 「off turns every charging Grub into an ordinary Grub ... the room's counts, waves and spots stay the same」 |
| V7 | pass(模擬) | 上記 1、2。 |
| V8 | pass(模擬) | 「Every enemy fades in for 0.8 s ... does not move, does not attack, does not hurt you, and your swipes do nothing to it (no damage, no flinch).」「You are not pushed away from a spot, and the enemy can appear on top of you.」 |
| V9 | pass(模擬) | 「fires its first shot 1.0 s after it finishes fading in」。弾は 4.0、撃った瞬間の位置へ直進、1 ハート、壁で消え、敵を通り抜けて敵にダメージを与えない。 |
| V10 | pass(模擬) | 「Your own numbers」: 攻撃 1 ダメージ、回復 0.35 s。ダッシュ 0.25 s で 4 タイル、ずっと無敵、クールダウン 0.6 s、ダッシュ中の攻撃は終了時に出る。被弾 1 ハート、硬直 0.3 s、被弾から 0.8 s 後まで無敵。移動速度、攻撃の届く距離、大きさは変更なし。新しいボタンなし。前回から変わっていない。 |
| V11 | pass(模擬) | 「During the wind-up, charge and recovery, your swipes lower its HP only. It does not flinch, is not pushed back, and does not change direction, speed or timing.」「At 0 HP it dies immediately in any state.」歩いている突進型は 0.2 s 怯む。出現中は効かない。 |
| V12 | (a)(b)(c)(d) すべて pass(模擬) | (a) 部屋 2: 「the second wave cannot come until it begins fading in. After that it comes when the Grub is dead, or 15 s after it finished fading in.」(b) 部屋 1: 左だけが待つ例が書かれている。1 体以下ならすぐ波 2、そうでなければ「after one is killed, or 10 s after the later one finished fading in」。(c) 「Each spot of a wave waits on its own. All spots of one wave start waiting at the same moment, when the wave is triggered. A spot that has finished waiting does not wait again」、4 タイル以上離れれば 2.0 s を待たずに出る。(d) 「Waves with no waiting spots start counting the moment they appear.」 |

F-1(再突進の待ち): 「at least 2.5 s have passed since its last recovery ended ... The 0.8 s of recovery is not part of the 2.5 s.」「if a charge ends at time t ... its next wind-up can begin no earlier than t+3.3.」「Flinching does not reset these waits.」「Recovery, 0.8 s」の項と「What play feels like now」の項(約 3.3 s 以上)も同じで、前回から変わっていない。

その他: 新しい音なし、新しいボタンなし(D-001 に抵触しない)。「Nothing flashes more than three times per second, apart from single flashes.」30/60 FPS は、ビルドが「同じ」と述べている点を読んだだけで、別々の観測はしていない。

### 観察(基準外。判定に入れない。原因は推測しない)

- **欠陥 D**: ビルドは今回も、「As before, occasionally, if you dash right after being hit, you take damage partway through the dash. This also applies to a charge that reaches you at that moment.」と書いている。欠陥 D は範囲外なので fail にしていない。Play の「抜けた」と感じられるか(§6.2)に影響しうる。
- 用語: 前回指摘した「front-left」は、ビルド 0.6 に見当たらない。他の箇所と同じ far-left / far-right の表記に揃っている。

## Decisions already made

- D-005: 怯み、接触、遠い方の規則(同距離は FL)。V7、V3、V4、V11 の判定の基準にした。
- D-008: 判定は模擬ビルドに基づく。結果に模擬であることを明記した。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。V7、V12 の判定の基準にした。

## Constraints

- この報告は模擬ビルドの記述に基づく。実機の証拠として扱わない。
- 見た目の A 系の基準は `art-director` の担当で、この報告の範囲外。
- QA は仕様の期待値を決めない。

## Open questions

1. **欠陥 D**: Play の前に規則を決めるか、既知の欠陥として Play に渡すか。Handoff 30、34 から引き続き、Studio の判断。
2. 実機でしか確認できない点: V3 の窓の端の数値(0.05 s 外れると被弾)。30/60 FPS の実測。等距離の位置でのログによる FL の確認。いずれも H1〜H4 とあわせて Play 以降で扱うかは、Studio の判断。

## Expected output

Studio が、この pass を受けて Play(`playtester`)の Handoff を組む。基準(§6.1)や実装の履歴は含めない。欠陥 D の扱いは上の Open questions 1 のとおり。

## Load

- Role: none (Studio が読む)
- Skills: none
- Project: design/combat.md、sim/build-0.6.md
- Decisions: decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/40-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 40
from: art-director
to: studio
stage: Play
outcome: pass
---
# 40: art-director → studio — 模擬ビルド 0.6 の視覚レビュー結果(突進の予告の見た目)

## Task

`design/grub-charge-telegraph.md`(D-006)の視覚受け入れ基準 A1〜A13 に対する `sim/build-0.6.md` の判定を受け取り、次の Play の Handoff を組む。判定は pass。ただし、実機でしか確かめられない項目と、ビルド記述にない項目が残る。これらは Play へ持ち越す。

## Context

- G-001(戦闘の単調さの改善)の Verify の視覚側。`qa` は規則と数値を確認済みで、全基準 pass(模擬)だった。
- **この判定はすべて「模擬ビルド `sim/build-0.6.md` の記述に基づく」。** D-008 により、実際の画素、実時間の見え方、実機での読み取りは確認していない。「確認不能(実機要)」と書いた項目を、記述から推測して pass にはしていない。
- 戦闘の規則・数値・タイミングは変更していない。仕様と D-006 も変更していない。新しい D-NNN は不要だった。権限内で決めるべき曖昧さはなく、規則の変更を要する点もなかった。

## Findings

### 1. 基準ごとの判定(A 系)

引用はビルド記述(英語原文)から。

| 基準 | 判定 | 根拠(記述) |
|---|---|---|
| A1 最初の描画からレーン(35% 以上) | pass | 「A red-orange lane appears on the floor … The lane fades from 35% to full brightness over the wind-up.」手順は Wind-up → Charge の順で、Charge の開始条件に Wind-up の省略はない。出現直後、Recovery 後、被弾中、ポーズ復帰後を個別に書いた文はないが、手順と開始条件から矛盾はない。個別の確認は `qa` の V1 の範囲。 |
| A2 レーンの向き = 突進方向、動いても変わらない | pass(定性) | 「toward where you were when the wind-up began」「The direction is fixed; moving afterwards does not turn the lane.」「rushes along the lane」。±3° の数値は記述にない。数値は確認不能(`qa` の測定項目)。 |
| A3 幅 ±0.1 タイル、長さ 7.0 または壁まで | pass | 「7 tiles or less if a wall is in the way, and as wide as the Grub's body (within 0.1 tile)」。 |
| A4 不透明度 35%→100% の単調上昇、FPS 差 5% 以内 | pass(定性) | 「fades from 35% to full brightness over the wind-up」。時間はすべて実時間で、30/60 FPS の差は約 0.034 s 以内と書かれている。「5% 以内」の数値は記述にない。数値は確認不能。 |
| A5 最暗の床でレーン縁の明暗比 3:1 以上 | **確認不能(実機要)** | 「It stays lit regardless of floor darkness」は意図の記述にとどまり、比は測れない。実機で確認する。 |
| A6 沈み込みと熾火が 0.7 s で完了 | pass | 「Wind-up, 0.7 s」「squashes to 80% height」「The ridge and eyes warm from dark to red-orange, turning pale-yellow in the final 0.1 s」。ease-in の指定は記述にない。 |
| A7 攻撃を当てても演出が変わらない | pass | 「your swipes lower its HP only. It does not flinch, is not pushed back … It flashes white for 0.1 s with small sparks … The lane and ridge do not change.」1 HP の傷の重ね絵は仕様 §8 の範囲内。 |
| A8 倒すとレーンと点灯が 0.1 s 以内に消える。ポーズで停止し続きから再開 | pass(レーンとポーズ)/点灯は記述なし | 「A dying winder or charger removes its lane within 0.1 s」「Pausing freezes all timers and animations, including lanes, steam and rings.」点灯(尾根、目)の消去は明記がない。死亡時の体の扱いが記述にないためで、矛盾ではなく欠落。 |
| A9 弾はレーンの上に描く。縁と矢印の一部が見える | 部分 pass/一部 **確認不能(実機要)** | 描画順は「Spitter shots, fading-in enemies and other enemies are drawn on top of it.」で pass。弾の下から縁と矢印が見えるかは、弾の見た目(大きさ、形)がビルド記述にないため判断できない。 |
| A10 5 つの見た目が 1 枚で区別できる | pass(記述上)/実画面は **確認不能(実機要)** | 出現中は半透明+青い輪、Wind-up はレーン+熾火+沈み込み、Charge は伸びた体+残像+土煙、Recovery は不透明+灰青+蒸気、歩きは変化なし。特徴が重ならない。ただし出現中と Recovery はどちらも青系(§3 の R3)。実際の見分けやすさは実機で確認する。 |
| A11 尾根が全状態で見える。通常型には付かない | 部分 pass/Charge 中は **記述なし** | 「visible from the moment they fade in. Ordinary Grubs have no ridge.」Wind-up は点灯、Recovery は「Ridge and eyes go dark within 0.1 s」。Charge 中の尾根の表示は書かれていない。 |
| A12 突進スイッチ off で演出なし | pass | 「off turns every charging Grub into an ordinary Grub, with no ridge, no lane and no charge」。 |
| A13 抜けた合図は無敵で抜けたときだけ | pass | 「A thin pale white-blue ring appears around you for 0.15 s」(無敵時)。被弾時は「No ring appears.」 |

### 2. 読みやすさ(visual-review の手順 1)

- **色だけに頼らないか**(combat.md §3.4、§10): pass(記述上)。次の組み合わせで伝わる。歩行アニメーションの停止、レーンの形と矢印、沈み込み、熾火の点灯、方向の固定。音は「No new sounds」で、音なしで読める設計は成立している。
- **レーン・熾火が他の要素と混同されないか**(Open question 3): **確認不能(実機要)**。ビルド記述は Spitter の弾の色と形を書いていない(既存アセットで、変更点でないため)。仕様 §2、§12 も「近ければ値だけ変える」未確認の項目としている。記述上は、レーンが帯+縁取り+矢印、弾が別物で、描画順は弾が上。形で区別する前提は崩れていない。他の脅威の表示は 0.6 に増えていない。
- **点滅**: 「Nothing flashes more than three times per second, apart from single flashes.」単発のフラッシュはレーンの Charge 開始時だけ。白い被弾フラッシュは攻撃の回復 0.35 s で上限が決まる。複数の合図が重なる部屋 5 の実際の頻度は、実機で確認する。

### 3. 一貫性(手順 2)と赤橙の使い方(Open question 2)

**赤橙の使い方: 違反なし。**

| 状態 | 色 | 判定 |
|---|---|---|
| 出現中 | 淡い青の輪、半透明 | 赤橙なし |
| Wind-up | 赤橙のレーン、熾火、目 | 「これから害になる」状態 |
| Charge | 赤橙の縁、核の芯 | 「いま害になる」状態 |
| Recovery | 灰青の沈んだ色、蒸気。尾根と目は消灯 | 赤橙なし |
| 歩行中の尾根 | 暗い赤茶(待機色) | 脅威の赤橙ではない。意図どおり |
| 抜けた合図 | 白青の輪 | 赤橙なし |
| 被弾フラッシュ | 白 | 赤橙なし |

形の言語(帯、矢印、輪)と、暖色=脅威/寒色=無害の使い分けは、美術方針(暖かい光と冷たい青黒の対比、脅威は彩度の高い橙〜赤)と一貫している。

### 4. 欠落と懸念の切り分け(Open question 1)

**ビルド記述の欠落**(矛盾ではない。ビルドの修正は求めない):

- G1: Charge 中の尾根の表示(A11)。
- G2: 倒されたときの熾火(点灯)の消去(A8)。
- G3: Wind-up 中のシェブロンが動かないこと(仕様 §5.1)。記述は「a chevron every tile pointing along the lane」だけ。
- G4: Spitter の弾の見た目(A9 と混同の確認に必要)。
- G5: A2 の ±3°、A4 の 5% など、数値の許容差。数値は `qa` の測定項目で、模擬の記述には現れない。

**仕様側の懸念**(規則の問題ではない。Play で確認する):

- S1: 抜けた合図(淡い白青 #CFE8FF の細い輪、プレイヤーの周り)と、出現中の淡い青 #8FB8E8 の輪(敵の足元)は、形も色相も近い。仕様 §9 は被弾表現との区別だけを求めていて、出現中の輪との区別を検討していない。担い手(プレイヤーと敵)と長さ(0.15 s と 0.8 s)は違う。部屋 5 のように波の出現中とダッシュが重なる場面で混同が起きないかは、実機で確認する。**混同が確認された場合の修正方針**: 抜けた合図を輪でなく短い放射状の火花か弧にする。色は白寄りにする。これは見た目だけの変更で、規則には触れない。
- S2: 接触が解決した後も、Charge が続く間はレーンが赤橙の 100% のまま残る(核だけが暗くなる)。仕様どおりで、D-006 の「Charge は害になる状態」の範囲に収まる。ただし、無敵で抜けたあとにレーンの上に立つと「まだ危ない」と誤読されないかを Play で見る。誤読される場合は、解決後にレーンも暗い側へ落とす案を取る。接触結果の口(D-004)が必要で、規則は変えない。
- S3: Recovery の灰青と出現中の青が近い。A10 の区別は、半透明か不透明か、蒸気の有無に頼る。小さい画面での見分けは実機要。

### 5. 実機でしか確かめられない項目(Play へ持ち越す)

仕様 §12 の項目のうち、判断できなかったもの:

- 暗い床での 35% のレーンの読み取り(A5)。
- レーンの赤橙と、Spitter の弾の色、ランタンの光との区別。
- 0.7 s の予告を読んでダッシュまで入力できるか。足りない場合、見た目の強調では補えなければ `game-designer` へ戻す(`design/combat.md` §7)。
- Recovery の沈んだ見た目が「死にかけ」「無敵」と誤読されないか。
- レーン幅を判定に一致させた感触(かすり)。
- 抜けた合図が過剰にならないか(上の S1 も含む)。
- 小さい画面での、尾根の通常型との差。
- 30/60 FPS で同じに感じられるか。
- 色覚の差で、形と沈み込みだけで読めるか。

## Decisions already made

- D-006: 予告は「地面のレーン + 熾火の点灯 + 沈み込み」。赤橙は害になる状態だけ。この判定は D-006 に反していない。
- D-001: ワンボタン戦闘。ビルド 0.6 は「No new buttons」で一致している。
- D-008: 判定は模擬ビルドの記述に基づく。
- 今回、新しい決定(D-010)は作っていない。

## Constraints

- 次の Play の Handoff では、受け入れ基準(A 系、V 系)と、設計側の内部情報を Playtester に渡さない。体験の観点は、仕様 §10.2 と combat.md §6.2 のとおり、基準を知らせない形にする。
- 戦闘の規則と数値は変更しない。変えたい点が出た場合は、変更せずに指摘として返す。

## Open questions

- なし。ビルド記述の欠落(G1〜G5)は、次にビルド記述を直す機会があれば補う程度でよく、Play の前に直す必要はない。

## Expected output

Studio は次を行う。

1. 本 Handoff の判定(pass、模擬ビルドに基づく)を記録する。
2. Play の Handoff に、§1.5 の実機項目と S1〜S3 を**観察の観点**として渡す。基準を知らせない言い方にする。例: 暗い部屋で、レーンの向きと範囲が一瞬で読めたか。抜けたときに「抜けた」と感じたか。レーンの上に立ったとき、まだ危ないと感じたか。
3. Play で「0.7 s では足りない」が出て、見た目の強調で補えない場合は、`game-designer` へ規則の問題として戻す。S1、S2、Recovery の誤読が出た場合は `art-director` へ戻し、上記の修正方針で見た目だけを直す。

## Sender assessment

- 判定は「pass」。ただし確信度は中程度。fail にするほど仕様と違う記述は見つからなかった。仕様の A 系 13 件のうち、記述だけで確認が完結したものは A1、A3、A6、A7、A12、A13(A2、A4 は定性のみ)。A5 は確認不能。A8、A9、A10、A11 には、記述の欠落か実機要の部分が残る。
- 欠落を「記述上は書かれていないが、実装されているだろう」と推測して pass にはしていない。G1、G2 の影響は小さく、実装側が仕様どおりなら自然に満たされる範囲だが、模擬の記述に現れていない事実は残した。
- 懸念として最も重く見ているのは S1(輪の類似)と S2(解決後もレーンが赤橙のまま)。どちらも見た目だけで直せ、規則・数値・入力に触れない。D-006 の割り当ての方針も変わらない。今は未確認の懸念として Play に回すのが妥当と判断した。
- 規則の問題と判断したものはなく、`game-designer` への戻しもない。

## Load

- Role: studio(Studio 自身。ロールファイルなし)
- Skills: none
- Project: design/grub-charge-telegraph.md、sim/build-0.6.md
- Decisions: decisions/D-006-grub-charge-telegraph-visual.md、decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/39-studio-to-art-director.md
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

<<<FILE goals/G-001-combat-monotony/42-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 42
from: playtester
to: studio
stage: Review
outcome: done
---
# 42: playtester → studio — ビルド 0.6 の戦闘体験の観察報告

## Task

ビルド 0.6 をプレイヤー像として遊んだ観察を報告する。判定や解決策は含めない。次の Review の Handoff を Studio が組むための材料とする。

## Context

Goal G-001(戦闘の単調さ)に関するプレイ。Handoff 41 の指示で、ビルド 0.6 の部屋 1〜5 を、戦闘に注意を向けて遊んだ。プレイヤー像は、短時間で濃いランを求めるアクション好きで、回避と間合いには慣れ、コンボ表の暗記は好まず、主にゲームパッドで遊ぶ。

## Findings

### プレイ方法(実際に使った方法)

- 実機ではなく、ドライランの約束事に従った。`sim/build-0.6.md` の「プレイヤーに見える記述」を読み、その場面を遊んだつもりで体験を書いている。
- 入力は移動、スワイプ(攻撃)、ダッシュだけを想定した。開発用の部屋選択、突進オン/オフ、30/60 FPS 切替、ログは使っていない。
- したがって、以下の「感じたこと」は記述から思い描いた体験である。実際に手を動かして得た感触ではない。
- 確認できなかったこと:
  - 実時間の感触(0.7 秒の予告が長いか短いか、3.3 秒間隔がだれるか、など)
  - 画面での実際の見え方(レーンの視認性、床の暗さ、リング、湯気、残像の見え方)
  - ゲームパッドの操作感、スティックでの避けやすさ
  - 移動速度の具体値(記述に数値がなく、Grub の歩行速度 2.0〜2.4 と比べられない)
  - 音(新しい音はないと書かれているだけ)
  - 30 FPS と 60 FPS の違いの体感

### セッション概要

部屋 1 から 5 まで順に想定して遊んだ。部屋 1 と 3 は、波が 2 回に分かれる以外は以前に近い。部屋 2、4、5 では突進する Grub(背中に暗い燃え殻色の隆起がある個体)が出て、戦い方が変わった。

### 具体的な場面

1. **部屋 1(通常 Grub 3 体、同時最大 2)**
   - 左右に Grub が出て、倒すと奥から 1 体追加で出る。
   - 見たこと: 出現中の 0.8 秒は動かず、スワイプも効かない。
   - 感じたこと: 追加の 1 体が来るので少しだけ「次が来る」感じがあるが、やることは従来どおり。注意は上がらない。
2. **部屋 2(突進 Grub 初登場)**
   - 最初の波は、奥に隆起付きの Grub が 1 体。
   - 見たこと: 3〜6 タイル離れた位置にいると、Grub が止まり、床に赤橙のレーンが伸びる。約 0.7 秒後、レーンに沿って走ってくる。
   - 感じたこと: レーンを見てから横に動くか、ダッシュで抜けられる。「見てから避ける」場面が自然に生まれる。コンボ表の暗記は要らない。
   - ダッシュで Grub をすり抜けるとダメージを受けず、白青い輪が出る(0.15 秒)。ダッシュ(0.25 秒の無敵)が狙いどおりに効いたと分かる合図になる。
   - 突進中にスワイプしても HP が減るだけで止まらない。白く光って火花が出る。「当たったのに止まらない」感じがある。
   - 2 発(HP 2)で倒せる。スワイプの硬直は 0.35 秒。
3. **隅で立ち止まってスワイプするだけの戦い方**
   - 記述の限りでは、部屋 2、4、5 では通用しない。レーンが出て、約 0.7 秒後に突っ込まれる。
4. **突進の間隔**
   - 1 体なら、前回の突進終了から約 3.3 秒以上あとに次の予告が出る。これは「突進→待つ→突進」の拍があるという意味。
   - 実際に退屈か、ちょうどよいかは確認できなかった。
5. **突進が来ない距離**
   - 記述上、Grub から 3 タイル未満に張り付くか、6 タイルより離れると、突進は始まらない。その間、普通の Grub のように歩いて噛むだけに見える。
   - 近づいて殴り続ければ、突進を一度も見ずに済む可能性がある(記述からの読みで、実際には試していない)。
6. **部屋 3(Spitter 初登場に近い構成、通常 Grub と Spitter)**
   - Spitter は動かず、2.0 秒おきに撃つ。弾速は 4.0 で、撃った瞬間の自分の位置を狙う。1 ハート減る。
   - 感じたこと: 動き続ければ避けられそう。出現後 1.0 秒は撃たないので、最初の一発の前に落ち着ける。
   - 第 2 波の Spitter は、自分から遠い奥の隅に出る。近づくのに距離がある。
7. **部屋 4(Spitter + 突進 Grub + 通常 Grub、同時最大 3)**
   - 弾を避けながら突進レーンも見る必要が出る。
   - レーンは Spitter の弾や他の敵より下に描かれる。弾と重なると見づらくなるかもしれないが、実際の見え方は確認できなかった。
   - 第 2 波は右奥の隅の Spitter と右の突進 Grub。
8. **部屋 5(6 体、同時最大 4、Spitter は 1.6 秒おき、Grub 歩行 2.4)**
   - 一番忙しい。弾、歩いてくる Grub、突進が重なる。
   - 第 2 波で左右に突進 Grub が 2 体出る。同時に条件を満たしても突進するのは 1 体ずつで、先に動くのはどちらか分からない順序(記述に「目立たない決まった順」とある)。
   - 感じたこと: 2 体同時に突進されないのは助かる。ただし「どちらが先か」を読めない。
9. **出現位置の近くに立つ**
   - 出現点の 4 タイル以内にいると、その敵は最大 2.0 秒出てこない。その間、次の波も始まらない。
   - 部屋 1 で左の出現点だけに近づくと、右の Grub だけが出て、左の Grub は遅れて出る。
   - 見たこと: 出現を待たせても押し出されない。出現した敵が自分の真上に出ることがある。出現中の 0.8 秒は無害だが、その後すぐ噛まれうる。
   - 感じたこと: 「敵が出てこない」ことに戸惑う可能性がある。待ちが見えるのかは確認できなかった。
10. **被弾直後のダッシュ**
    - 記述に「以前と同様、被弾直後にダッシュすると、ダッシュの途中でダメージを受けることがある」とある。突進が当たる瞬間にも同じことが起きうる、と書かれている。
    - 不具合らしい挙動として、観察のままここに記す。実際に起きるかは確認できなかった。

### 問題と影響度

| # | 内容 | 影響度 |
|---|------|--------|
| A | 部屋 1、3 は戦い方が前と変わらず、第 2 波が来るだけ。戦闘の変化は部屋 2、4、5 に集中している | 中(記述からの印象) |
| B | 突進 Grub に 3 タイル未満で張り付く、または 6 タイルより離れると突進が出ない。突進を見ずに済む戦い方がありうる | 中(試していない) |
| C | 突進中のスワイプは「効いているのに止まらない」。フィードバックはあるが、当たった手応えは薄そう | 低〜中(実際の感触は確認できなかった) |
| D | 出現点の近くに立つと敵が最大 2.0 秒出ず、次の波も遅れる。理由がプレイヤーに伝わるか不明 | 低〜中 |
| E | 被弾直後のダッシュで、無敵のはずが途中で被ダメージ(既知の挙動として記述あり) | 高になりうる(突進を避けるためのダッシュに影響する) |
| F | 部屋 5 は敵の種類が重なり、突進の順序も読めない。忙しさが公平な難しさか、運任せかは確認できなかった | 不明 |

### よかった点

- 予告(レーン、しゃがみ込み、色の変化)があり、見てから避けられる設計に見える。
- 背中の隆起で、突進する個体が出現直後から見分けられる。
- ダッシュで抜ける、横に避ける、という既存の操作だけで対応できる。新しいボタンも覚えることもない。
- 突進は同時に 1 体だけなので、最悪の重なりは避けられている。
- 突進後の「湯気を出して止まる」回復の時間(0.8 秒)が、反撃のチャンスとして読める。

### 観察とは分けた仮説(原因の推測)

- 部屋 2、4、5 での「立ち止まりスワイプの無効化」が、戦闘の単調さを減らしている可能性がある。ただし、実際に飽きにくくなったかは、実時間で遊ばないと言えない。
- 「近づき過ぎると突進しない」性質が、新しい単調さ(張り付き戦法)を生むかもしれない。

### プレイヤーとしての未解決の疑問

- 突進 Grub に張り付いたときも、予告なしに突進されることはないのか。
- 被弾直後のダッシュで途中被弾するのは、どのくらいの頻度で起きるのか。
- 出現を待たされているとき、画面でそれと分かるのか。
- 部屋 5 の 2 体の突進 Grub は、どちらが先に動くのか読めるのか。

## Decisions already made

None

## Constraints

- 観察は `sim/build-0.6.md` を読んで想定した体験である。実時間、見た目、ゲームパッドの感触、音は確認できなかった。
- 原因の推測と設計案は、観察と分けて書いた(仮説の節のみ)。

## Open questions

None

## Expected output

Studio が、この観察報告から次の Review の Handoff を組む。判定や解決策の決定は、この報告には含めていない。

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile、sim/build-0.6.md
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/41-studio-to-playtester.md
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
