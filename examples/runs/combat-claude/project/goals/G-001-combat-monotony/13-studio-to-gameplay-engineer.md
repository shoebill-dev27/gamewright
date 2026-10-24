---
kind: handoff
goal: G-001
seq: 13
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 13: studio → gameplay-engineer — 予告つき Grub 突進と部屋の波・進行を実装する(T0 調査から)

## Task

`design/combat.md` と `design/grub-charge-telegraph.md` の仕様どおりに、D-004 の技術方針で戦闘を変更する(予告つき Grub 突進、部屋の構成と進行、突進の予告の見た目)。最初に T0(既存の仕組みの調査)を行い、前提が崩れたら実装に入らず Studio に戻す。仕様が曖昧・矛盾・欠落している場合は自分で決めず、`outcome: question` で返す。

## Context

Goal G-001「戦闘の単調さの改善」。D-002 で、主軸は部屋の構成と進行、敵の挙動の追加は予告つき Grub 突進の 1 つだけと決まった。仕様は `design/combat.md`(D-003、D-005 で確定)、技術方針は D-004、突進の予告の見た目は `design/grub-charge-telegraph.md`(D-006)。ここまでの Design と Plan は完了している。実装後は `qa`(verify-change)と `art-director`(visual-review)が並列で検証し、その後 Playtest、Review に進む。

## Findings

(Studio が、視覚仕様の客観的な内容を前段の成果から抜き出した。数値・詳細は仕様ファイルが正。)

### T0 で最初に確認すること

- 部屋データ、スポナー、弾の衝突、接触の判定形状が、D-004 の見積もりどおりか(D-004 は `sim/` の記述に基づく見積もりで、コードは読んでいない)。
- 部屋のコードと敵のコントローラが別モジュールか。別なら、部屋・波の作業(T2)と突進の作業(T3)を並列にしてよい(独立した作業ツリーは、D-004 の計画に従う場合のみ)。
- 視覚要素の既存の仕組み: 地面層に半透明の帯を描けるか、スプライトの色変調と変形(拡大縮小・描画ずらし)ができるか、重ね絵ができるか、敵の HP 表示と被弾フラッシュの有無、既存の出現演出、粒子、Spitter の弾の色。

### 突進の予告の視覚要素(詳細は `design/grub-charge-telegraph.md` §11)

- 必須:
  1. 突進型の状態・経過割合・突進方向を見た目の側から取れること。
  2. 地面のレーン(半透明の帯、縁取り、矢印)。幅は接触判定と一致、長さは 7.0 タイルまたは壁まで。不透明度は Windup の間に 35%→100%。
  3. スプライトの色変調、拡大縮小、描画ずらし(沈み込み、Charge の伸び)。
  4. 熾火の尾根の重ね絵(Windup で点灯。突進型は消灯した尾根で常時区別)。
  5. 被弾の白いフラッシュ。怯みの動きは使わない(D-005)。
  6. 出現中の淡い青の半透明と輪。
- 望ましい: 7. 残像・土煙・蒸気の粒子、8. 敵に HP 表示がなければ傷の重ね絵、9. 接触の結果(無敵で抜けた/被弾)の通知(抜けた合図と使用済み表示に使う)。
- あれば: 10. 音(溜め音、息の音。音が予定範囲にある場合のみ)。
- 全部の変化は状態の経過割合から求め、30 FPS と 60 FPS で同じ長さに見えること。色だけ・音だけに頼らない。赤橙は害になる状態だけに使う。
- 新しい大きなアセットは不要の見込み。小さな新規素材は、矢印 1 枚、尾根の重ね絵、必要なら傷の重ね絵と粒子 1 種。
- 要素 3 が使えない場合の縮小案、要素 2 の代替案は仕様 §11 にある。要素 7〜9 は、省いても必須は成立する。
- 色の値は暫定値で、Spitter の弾の色などを確認してから調整してよい(方針は変えない)。

### 未確認の点(Play で確認する。実装では仕様どおりに作る)

0.7 s の予告で読んでダッシュするのに足りるか、暗い床での読み取り、レーン幅と判定の一致の感じ方などは、実機のプレイで確認する。数値は暫定値として扱い、調整しやすい形(データ・定数)にしておく。

## Decisions already made

- D-001: 攻撃とダッシュだけのワンボタン戦闘。新しい入力ボタンは Owner 承認なしでは不可。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進の 1 つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない。
- D-003: 突進は同時に 1 体・方向固定・予告中は無害。部屋は突進スイッチで外せる。
- D-004: 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ。
- D-005: 突進型は 3 状態で怯まない。接触は突進ごとに最初の重なりで 1 回だけ解決する(解決済みフラグ)。「遠い方」は出現を決める時点で選ぶ。これらはデータ・状態の規則として実装する。
- D-006: 予告は「地面のレーン + 熾火の点灯 + 沈み込み」。赤橙は害になる状態だけ。突進型は尾根で区別。被弾は白いフラッシュ。

## Constraints

- 30 FPS と 60 FPS の両方で正しく動くこと(時間は実時間・経過割合で扱う)。
- 小さなチームのため、既存の仕組みの再利用を優先する。
- 新しい入力ボタンは足さない(D-001)。開発用補助(部屋の選択、突進スイッチ、30/60 FPS 切り替え、状態の遷移ログ)は開発ビルド限定とし、プレイヤー向けの入力は足さない。
- 戦闘の規則と数値を自分で変えない。仕様と食い違い・不足があれば返す。
- この Handoff には欠陥 D(被弾直後のダッシュ中のダメージの疑い)の修正は含まない。`qa` の再現がまだ無く、原因も確定していないため。
- リポジトリ・ビルドの扱いは `sim/repo-notes.md` と `sim/build-0.3.md` に従う(サンプルプロジェクトで、ビルドは `sim/` で模擬される)。

## Open questions

- 要素 9(接触の結果の通知)が D-004 の「見た目への口」に含まれるか。含まれず、追加も難しいなら、勝手に省かず結果を返す(省く場合は、仕様 §6 の使用済み表示と §9 の抜けた合図が対象)。判断が技術方針に関わるなら Studio 経由で `technical-director` に回す。
- 必須の要素が既存の仕組みで実現できない場合は、縮小案(仕様 §11)で足りるか確認し、足りなければ返す。

## Expected output

- 変更と、ビルドの説明(何を変えたか、`qa` と `art-director` が検証するための動かし方、テストの結果、T0 の調査結果)。
- 結果は `studio` 宛て(`to: studio`)の Handoff で返す。次の工程 Verify(`qa` と `art-director` を並列)を Studio が独立な Handoff に組み直せるようにするため、実装側の自己評価は `## Sender assessment` にだけ書き、Findings には客観的な事実(変更点、動かし方、受け入れ基準ごとの自己テスト結果)を書く。
- `outcome`:
  - `done`: 実装を終えた。
  - `question`: 仕様が曖昧・矛盾・欠落している(Design へ)、T0 で前提が崩れた・計画が成り立たない(Plan へ)、または方向・スコープに関わる(Decide へ)。実装に入らず、または入った範囲を明記して返す。

## Sender assessment

Studio は内容の判断をしていない。Handoff 12(`art-director`)の Sender assessment は、渡さない方針(Build に不要)のためここには含めていない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/grub-charge-telegraph.md, project.md#constraints, project.md#art-direction, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-005-flinch-contact-and-far-slot-rules.md, decisions/D-006-grub-charge-telegraph-visual.md
- Previous handoff: none
