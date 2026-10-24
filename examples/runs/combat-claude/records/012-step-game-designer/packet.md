# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/09-studio-to-game-designer.md
next_seq: 10

## You may write

- goals/G-001-combat-monotony/10-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-005-<name>.md

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

<<<FILE goals/G-001-combat-monotony/09-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 9
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 09: studio → game-designer — 技術確認で見つかった仕様の食い違い 3 点に答え、必要なら `design/combat.md` を直す

## Task

`technical-director` が実現性を確認し、仕様の文面と既存実装の食い違いを 3 点見つけた。それぞれ仕様側の意図を決め、`design/combat.md` に明記する。あわせて下の既定 4 を確認する。仕様が決まらないと Build に進めない。特に 1 と 2 は V1、V3、V4 の合否に関わる。

## Context

Goal G-001(戦闘の単調さの改善)。D-002 の主軸は部屋の構成と進行で、併用は予告つき Grub 突進の 1 つだけ。D-003 で突進の規則と部屋ごとのスイッチが決まり、`design/combat.md` に仕様化された。

技術計画(Handoff 08)では、仕様は既存システムの範囲で実現できると判断された。ただし `sim/repo-notes.md` と `sim/build-0.3.md` の記述だけを根拠にしており、コードは読んでいない。技術側は仕様を書き換えず、仕様の文面どおりに作る前提で計画した。以下は、その前提が合っているかの確認である。

## Findings

### 確認依頼 1: 怯み(Flinch)

- 既存の敵は、被弾すると 0.2 秒の怯みに入り、Attack を含む行動を中断して Chase に戻る。
- `design/combat.md` の §2.1 と §8 は「怯みは既存のまま」と「(突進型は)被弾しても状態を中断しない」を同時に書いている。
- 技術側の前提: Spawning、Windup、Charge、Recovery の間だけ怯みを無効にする(ダメージは受ける)。Chase など他の状態の怯みは既存のままにする。
- 依頼: この解釈でよいか決め、§2.1 と §8 に怯みの扱いを明記する。

### 確認依頼 2: 接触の定義

- Charge 中の Grub の体は、接触の開始後もしばらくプレイヤーと重なり続ける。
- §3.5 と V3 のダッシュの窓(0.25 秒。接触の 0.25 秒前から接触の瞬間まで)は、接触を 1 点の瞬間として数えている。
- 技術側の前提(案 A): 突進ごとに、最初の重なりで接触を 1 回だけ解決する。
  - そのとき無敵ならダメージなしで、その突進はもうダメージを与えない。
  - 無敵でなければ 1 回だけダメージを与える。
- 案 B: 重なっている間ずっと判定する。この場合、窓は重なりの長さ(おおよそ 0.1〜0.2 秒)だけ狭くなる。
- 依頼: A か B かを決め、§3.5 と V3、V4 にその定義を明記する。窓の幅は、プレイで「ダッシュが使える」と感じられるかに直結する。窓の数値を変えるなら、その根拠も書く。

### 確認依頼 3: 部屋 5 の波 2 の「FL または FR」

- 部屋 3 の「プレイヤーから遠い方」と同じ規則でよいか。技術側は同じ規則で組む前提。データだけの変更で直せる。
- 依頼: 規則を決め、§4.3 に明記する。

### 既定 4(確認のみ)

確認なしで次の既定で進める。違う場合だけ直してほしい。

- 「出現中が終わってから T 秒」は、その波の最後の敵の出現中が終わった時点を起点にする。
- 「生きている敵」には出現中の敵を含める。
- 出現位置にプレイヤーが重なっても押し出さない。出現中の 0.8 秒は無害で、待ちは最大 2.0 秒(仕様どおり)。

### 参考(技術側の事実。判断材料として)

- 1 更新あたりの移動量: Charge は 30 FPS で約 0.27 タイル、60 FPS で約 0.13 タイル。ダッシュは 30 FPS で約 0.53 タイル。
- 接触の判定は、更新ごとのスイープ判定で FPS に依存しないようにする。時間の誤差は 30 FPS で 1 更新(約 0.034 秒)以内で、§0 の許容に収まる。
- 計画は無敵の挙動を変えない。無敵の読み取りは 1 つの問い合わせ関数を通す。欠陥 D(被弾直後のダッシュ中のダメージの疑い)は別ステップ(`qa` の再現)で、今回の仕様には含めない。V3、V4 の測定で、被弾直後のダッシュの窓は欠陥 D が確認されるまで外す前提になっている。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。新しい入力は足さない。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進のみ。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。部屋は突進スイッチで外せる。
- D-004: 技術方針(スイープ判定、delta の上限と余りの持ち越し、導出による同時 1 体、スポナーでのスイッチ、見た目への口、無敵の問い合わせ関数)。

## Constraints

- D-001〜D-003 の範囲内で決める。新ボタンは不可。突進以外の敵の挙動追加、プレイヤー側の数値調整、キット変更は D-002 の範囲外。
- 30 FPS と 60 FPS の両方で正しく動くこと。小さなチームのため、既存システムの再利用を優先する。
- 欠陥 D の規則(ダッシュと被弾後の無敵)は今回書かない。再現結果が出てから書き足す。
- 答えが D-002 や D-003 の変更、スコープの変更を要するなら、自分で決めず `game-director` に回す(`outcome: question`)。

## Open questions

- 確認依頼 1〜3 への答え(上記)。既定 4 の承認。

## Expected output

- `design/combat.md` を更新する(§2.1、§8、§3.5、V3/V4、§4.3 のうち該当箇所)。変えた箇所と理由を Findings に列挙する。新しい数値は暫定値と明記する。
- 決定が後続の作業を拘束する場合(特に確認依頼 2)は、`make-decision` に従って Decision を記録する。
- 結果は `to: studio` 宛ての Handoff で返す(次の Role は Studio が決める)。Playtester に渡さない前提で、仕様の数値や体験の観点を書いてよいが、実装情報と区別して書く。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md(§2.1、§3.5、§4.3、§6、§8、§9), project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md
- Previous handoff: goals/G-001-combat-monotony/08-technical-director-to-studio.md
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
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

<<<FILE goals/G-001-combat-monotony/08-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 8
from: technical-director
to: studio
stage: Route
outcome: done
---
# 08: technical-director → studio — 戦闘仕様は既存システムの範囲で実現できる。技術計画と、設計者への確認 3 点を回す

## Task

技術計画(確認事項への回答、リスク、テスト方針、順序、並列化の可否)を受け取り、次の宛先を決める。`art-director` の結果と合わせて Build に進める。ただし Build の前に、下の「仕様の確認依頼」を `game-designer` に回すこと。

## Context

Goal G-001。`design/combat.md`(§2〜4、§6、§9)の実現性を確認した。調べたのは `sim/repo-notes.md` と `sim/build-0.3.md` の記述で、**コードそのものは読んでいない**。部屋データ、スポナー、弾の衝突、接触の判定形状は記述にないため、下では「前提」と書き、最初の作業(T0)で確認する。

## Findings

### 結論

- 仕様は D-001〜D-003 と制約(30/60 FPS、小さなチーム、再利用)の範囲で実現できる。範囲外の費用や不可逆な作業はない。`outcome: question` にはしない。
- 全体の大きさは中程度。新しい仕組みは、敵の状態(出現中、Windup、Charge、Recovery)、波の管理、部屋データの拡張、スイープ判定の 4 つ。
- 仕様と既存実装の食い違いが 2 件ある(下の「仕様の確認依頼」)。技術側では仕様を書き換えず、仕様の文面どおりに作る前提で計画した。

### §9 の確認事項への回答

| # | 問い | 回答 | 費用 |
|---|---|---|---|
| 1 | Grub に状態を足せるか。接触ダメージを状態で切り替えられるか | 可能。敵は 1 つの共通コントローラ(Idle / Chase / Attack)で、種別ごとの違いはデータと小さな攻撃ルーチンで持つ。ここに Spawning、Windup、Charge、Recovery を足し、突進型を `grub_charger`(Grub のデータ + 突進の数値)として定義する。接触ダメージを Chase と Charge だけで有効にする。**前提**: 噛みつきの判定が Attack のルーチン側にあり、状態で切れる。T0 で確認する。 | S〜M |
| 2 | 30 FPS で接触を取りこぼさないか | 現状の重なり判定だけでは保証できない(下の「判定の取りこぼし」)。スイープ判定を足せば保証できる。 | S |
| 3 | 同時に予告できる突進を 1 体に制限できるか | 可能。保存する状態は作らない。Windup に入る瞬間に、生きている他の突進型が Windup または Charge にいるかを調べる(敵は最大 4 体)。倒された敵は、HP が 0 になった時点で生存一覧から外す。同時に開始する場合は更新順で先の 1 体が取る。 | S |
| 4 | 部屋データで指定できるか | **部屋データの現状は記述になく、確認できない**(T0)。最小の拡張案は下の「部屋データ案」。突進スイッチは、スポナーが `grub_charger` を `grub` に置き換える 1 か所で実現する。 | M |
| 5 | 「最初に全部出す」前提か | **確認できない**(T0)。波に対応するには、部屋の終了条件を「すべての波が出現済みで、生きている敵が 0」に変える必要がある。これは部屋コントローラの変更で、扉やクリア演出など終了に紐づく処理が付いていれば波及する。 | M(波及しだい) |
| 6 | 秒の経過時間で進めているか | 可能性が高い。ループは可変 delta time で、プレイヤーのタイマーも秒、敵の怯みも 0.2 s。ただし Spitter の間隔と移動が秒かは未確認(T0)。ポーズ復帰の最初の更新に大きな delta が入る危険があるため、delta の上限(0.05 s)を設ける。 | S |
| 7 | 弾が壁で消え、敵を通り抜けるか | 記述にない(T0)。弾が壁とプレイヤーの層だけに当たる設定にすればよい見込み。 | S |

### 判定の取りこぼし(§9-2)

- 1 更新あたりの移動量: Charge は 30 FPS で約 0.27 タイル、60 FPS で約 0.13 タイル。ダッシュは 16 タイル/s なので、30 FPS で約 0.53 タイル。向かい合うと相対で 24 タイル/s、30 FPS で約 0.8 タイル。
- 接触の判定形状の大きさは仕様でも未定義(§8)で、ここでは確認できない。0.8 タイルは小さな判定を飛び越える可能性がある大きさ。
- **方針**: Charge 中の接触は、更新ごとに「Grub とプレイヤーの移動を相対運動として、更新の始点から終点まで」スイープ判定する。判定の形が円でない場合は、相対移動が 0.25 タイル以下になるよう分割する。
- 時間の扱い: 状態のタイマーは更新の delta を足して進め、状態の切り替わりでは余りを次の状態に持ち越す。これで状態の長さは 30 FPS で 1 更新(約 0.034 s)以内の誤差になり、仕様の許容(§0)に収まる。
- Charge の距離: 7.0 タイルちょうどで止める(最後の更新は距離で切る)。壁は、実際の移動量が要求量より小さかった時点で終了とする。「壁で止まる」既存の動きが壁沿いに滑る場合でも、突進は滑らず終わる。
- 更新の順序は、プレイヤー(入力、ダッシュ、無敵)→ 敵の移動 → 接触の解決 とする。順序が一定なら FPS による接触の有無の差は 1 更新以内に収まる。
- ダッシュ中の無敵は、既存の無敵フラグを読むだけにする。読み取りは 1 つの問い合わせ関数を通す。

### 部屋データ案(最小の変更)

- 部屋ごと: `grubSpeed`、`spitterInterval`、`chargeEnabled`、`slots`(Door / Far / L / R / FL / FR の座標)、`waves[]`。
- 波ごと: `spawns[{type, slot}]`(type は grub / grub_charger / spitter)、`next{K, T}`。「FL または FR のうち遠い方」は、スロットのリストと選択規則で書く。
- 全部屋共通の定数: 出現中 0.8 s、出現位置の待ち(4 タイル未満なら最大 2.0 s)、Spitter の最初の 1 発 1.0 s、弾速 4.0。部屋データには入れない。
- `chargeEnabled=false` のときは、スポナーが生成時に `grub_charger` を `grub` に置き換える。敵の数、波、位置は変わらない(V6)。
- 部屋データが既存の形式と大きく違う場合は、T0 で戻す。

### 技術的リスクと対策

| リスク | 対策 |
|---|---|
| R1 既存の Flinch(敵が被弾すると 0.2 s の怯みで Attack を含む行動を中断し Chase に戻る)が、仕様の「被弾しても状態を中断しない」(§2.1)と食い違う | 仕様の文面どおり、Spawning、Windup、Charge、Recovery では Flinch に入らない(ダメージは受ける)。Chase など他の状態の Flinch は既存のまま。確認を依頼する。 |
| R2 接触の定義。§3.5 と V3 の窓(0.25 s)は、接触を 1 点の瞬間として数えている。Grub の体は接触の開始後も重なり続ける | 下の確認依頼 2。解釈しだいで窓の幅が変わる。 |
| R3 取りこぼし、delta のばらつき、ポーズ復帰の大きな delta | スイープ判定、delta の上限、余りの持ち越し。ポーズ復帰の更新は V1 で確認する。 |
| R4 部屋データ、スポナー、終了条件の結合が強い | T0 で確認。強ければ T3 を拡大するか、仕様の波の使い方の再確認のために戻す。 |
| R5 無敵の実装を触ると、欠陥 D の調査と混ざる | この計画は無敵の挙動を変えない。読み取りの問い合わせ関数を足すだけにする。欠陥 D の修正は別の作業で、その関数の裏側を変えるだけで済む。D が再現された場合、被弾直後のダッシュの窓を V3/V4 の測定から外す。 |
| R6 突進中の敵どうしの通り抜け(仕様 §2.1)で、他の敵の押し合いが変に動く | 突進中の Grub は敵どうしの分離から除外する。他の敵は押さない。T2 でテストする。 |
| R7 出現位置にプレイヤーが重なった場合 | 押し出しは作らない。出現中の 0.8 s は無害で、見えるので動ける。待ち(最大 2.0 s)も仕様どおり。確認依頼 4 に記載。 |
| R8 セーブデータの互換 | 部屋の進行だけを持つ場合は影響なし。波の途中の状態を保存していないことを T0 で確認する。 |
| R9 art との接点。予告の見た目は art-director の別ステップ | 敵の状態、状態の経過割合、突進の方向を見た目側に渡す口を T2 で作る。art の結果が来るまでは、デバッグ表示(予告の線と停止)で代用する。柱3 の最終確認は実機の Play。 |

### テスト方針

**自動(今は敵と無敵のテストがないため新規)**

- 敵コントローラと波の管理を、固定 1/30 s、固定 1/60 s、ばらつく delta で進める検証用の枠。
- 状態の長さ(Windup 0.7、Recovery 0.8、出現中 0.8)が許容内(V1、V8)。Charge の速度と距離、方向の固定(V2)。接触ダメージが Chase と Charge のみ、1 回の突進で 1 回まで(V4)。
- スイープ判定: 距離を細かく変え、30 FPS と 60 FPS で接触の有無が一致する。ダッシュの窓: 開始時刻を接触の前後でずらし、境界が 30 FPS の 1 更新以内で一致する(V3)。
- 同時 1 体: Windup 中に倒す、Charge 中に倒す、同時に開始する(V5)。スイッチのオン/オフで敵の数、波、位置が同じ(V6)。
- 部屋データが §4.3 の表と一致する(V7)。弾の速度、最初の 1 発、壁、敵の通り抜け(V9)。
- プレイヤー側の定数(攻撃 0.35 s、ダッシュ 0.25 s・4 タイル・0.6 s、被弾 0.3 s・0.8 s)が変わっていない(V10)。定数だけを固定する。欠陥 D の挙動は固定しない。

**QA が実機で確認**

- V1〜V10 を 30 FPS と 60 FPS の両方で。特に V1 のポーズ復帰後、V3 の実際の入力、V8 の見え方。
- そのために、開発ビルド限定の補助を足す: 部屋の選択、突進スイッチの切り替え、FPS の 30/60 切り替え、状態の遷移ログ。これらは出荷ビルドに入れない。プレイヤー向けの新しい入力は足さない(D-001)。
- 体験の観点(§6.2)は Play で見る。

### 順序

1. **T0 調査(S)**: コントローラ、スポナー、部屋の終了条件、弾の衝突、delta とポーズ、判定形状、セーブを確認する。前提が崩れたらここで戻す。
2. **T1 土台(S〜M)**: delta の上限とポーズ復帰、検証用の枠、プレイヤー定数のテスト、無敵の問い合わせ関数(挙動は変えない)、T2/T3 の境界(生成の引数、倒れたときの通知)。
3. **T2 敵(M)**: Spawning、Windup、Charge、Recovery、Flinch の除外、同時 1 体、スイープ判定、見た目への口、Spitter の最初の 1 発、弾の確認。
4. **T3 部屋(M)**: スキーマ、波の管理、スロット、出現待ち、突進スイッチ、部屋ごとの数値、終了条件の変更。
5. **T4 統合とデータ(S)**: 合流、§4.3 の 5 部屋を入力、V7 の自動テスト。
6. **T5 QA 準備(S)**: 開発用補助。そのあと QA へ。

依存: T0 → T1 → (T2 ∥ T3) → T4 → T5。art の結果は T4 以降で組み込む。

### 並列化

- **T2 と T3 は並列にできる(条件つき)。** 変更するコードが分かれる。T2 は敵のコントローラと種別データ、T3 は部屋、スポナー、データ。境界は T1 で固定する小さなインターフェース 2 つ(生成の引数、倒れたときの通知)。理由は、どちらも中規模で独立して進められ、先に境界を決めれば合流の衝突が少ないため。
- 隔離した作業場所は T2/T3 の間だけ使う。
- **条件**: T0 で、部屋のコードと敵のコントローラが別のモジュールだと確認できること。同じファイルに絡んでいれば直列にする。出現中の状態と Spitter のタイマーは、衝突を避けるため T2 に置く。
- 無敵のコードは触らないので、欠陥 D の修正とは並列でも衝突しない。ただし V3/V4 の測定は混ざりうる(R5)。

### 仕様の確認依頼(game-designer へ。Build の前、V3 の前に必要)

1. **Flinch(R1)**: 既存の敵は被弾で 0.2 s の怯みに入り、行動を中断する。§2.1 と §8 は「怯みは既存のまま」と「状態を中断しない」を同時に書いている。計画は、Spawning、Windup、Charge、Recovery だけ怯みを無効にし、他は既存のままとして組む。この解釈でよいか。§2.1/§8 に Flinch を明記してほしい。
2. **接触の定義(R2)**: Charge 中の Grub の体は、接触の開始後もしばらくプレイヤーと重なる。§3.5 と V3 の窓(0.25 s、接触の 0.25 s 前から瞬間まで)を成り立たせるには、突進ごとに最初の重なりで接触を 1 回だけ解決する必要がある。そのとき無敵ならダメージなしで、その突進はもうダメージを与えない。重なっている間ずっと判定すると、窓は重なりの長さ(おおよそ 0.1〜0.2 s)だけ狭くなる。計画は前者で組む。それでよいか。
3. **部屋 5 の波 2 の「FL または FR」**: 部屋 3 の「プレイヤーから遠い方」と同じ規則でよいか。計画は同じ規則で組む。データだけの変更で直せる。

次の 2 点は影響が小さいため、確認なしで次の既定で進める。違えば知らせてほしい。

4. 「出現中が終わってから T s」は、その波の最後の敵の出現中が終わった時点を起点にする。「生きている敵」には出現中の敵を含める。出現位置の重なりは押し出さない(R7)。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。開発用補助は出荷ビルドに入れず、プレイヤー向けの入力を足さない。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進のみ。
- D-003: 突進の規則と部屋ごとの突進スイッチ。
- D-004(今回、technical-director): 技術方針(スイープ判定、delta の上限と余りの持ち越し、導出による同時 1 体、スポナーでのスイッチ、見た目への口、無敵の問い合わせ関数)。

## Constraints

- 仕様は変えていない。上の確認依頼は仕様の変更の提案ではなく、仕様の文面と既存実装の食い違いの確認。
- この Handoff の Findings には実装の情報が入っている。Playtester には渡さない。
- 欠陥 D は別ステップ(`qa` の再現)。この計画では無敵の挙動を変えない。

## Open questions

- 上の確認依頼 1〜3(`game-designer`)。1 と 2 は V3、V4、V1 の合否に関わる。
- T0 の調査結果しだいで、部屋データとスポナーの結合が強い場合は、T3 の大きさと並列化の可否を見直す。その場合は新しい計画を Studio に返す。

## Expected output

- Studio は、確認依頼 1〜3 を `game-designer` に回す(Design)。`art-director` の結果と合わせて Build に進める。
- Build は T0 から始める。T0 で前提が崩れた場合は、Studio に戻す。
- Build のあと `qa` が §6.1 の V1〜V10 を 30 FPS と 60 FPS で確認する。

## Sender assessment

- 確信度: 実現性は中〜高。根拠は記述のみで、コードは読んでいない。特に部屋データ、スポナー、弾の衝突、接触の判定形状は未確認で、費用の見積もりはここが動く。
- 欠陥 D の仮説(`qa` には渡さない): 無敵が 1 つのフラグで、ダッシュと被弾の 2 つのタイマーが別々に切る。そのため、被弾後の無敵の途中でダッシュを始めると、先に切れるタイマーがフラグを落とし、ダッシュの途中で無敵が消えうる。突進が入ると、被弾直後に回避を試みる場面が増えるため、この欠陥に当たる頻度が上がる可能性がある。D が再現されたら、修正を Play の前に入れる方がよい。
- 確認依頼 2 は、窓の幅(Play でダッシュが「使える」と感じられるか)に直結する。仕様の数値を実機で見る前に決めておく価値がある。
- Owner のエスカレーションは不要。

## Load

- Role: none(Studio の routing)
- Skills: none
- Project: design/combat.md(§2〜4、§6、§9), project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md
- Previous handoff: goals/G-001-combat-monotony/07-studio-to-technical-director.md
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
