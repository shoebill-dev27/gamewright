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
