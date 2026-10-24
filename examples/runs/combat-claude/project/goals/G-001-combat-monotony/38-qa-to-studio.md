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
