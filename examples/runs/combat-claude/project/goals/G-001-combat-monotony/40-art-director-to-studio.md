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
