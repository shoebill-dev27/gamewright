# Studio operation packet

operation: Simulate (dry-run harness, not a Studio operation)
goal: G-001

## You may write

- sim/build-0.5.md
- sim/repo-notes.md

## Inputs

<<<FILE simulator-instructions
You are the dry-run build simulator. You are not a Studio Role and make no decisions.

The game does not exist; its build and code are described in text. A change was just implemented.
From the engineer's description of the change, the previous build description and the repository
notes, write two files:

1. The new build description: what a player and a tester can observe when they run the changed
   game, under every condition the project constraints name (for example each supported frame
   rate). Describe what would actually happen given the change as implemented, including any flaw
   the description implies — not what was intended. Player-observable behavior only: no design
   intent, no acceptance-criteria names, no implementation terms. Do not copy HTML comments.
   Write it as observations of the running build (by the project's dry-run convention, this text is
   the build); do not add notes about the simulation itself.
2. The updated repository notes: implementation facts after the change.

Write each file as a file block (<<<FILE <path> ... >>>END) using exactly the paths under
"You may write". Text outside file blocks is discarded.
>>>END

<<<FILE goals/G-001-combat-monotony/32-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 32
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 32: gameplay-engineer → studio — 変更内容 2.1〜2.4 の修正版(F-1 の起点の明記、Grub 速度の数値、同距離の規則、プレイヤー側の数値)

## Task

Handoff 31 の指示により、変更内容(2.1〜2.4)を修正して全体を書く。Handoff 28 を読まなくても分かる形にする。F-1、V7 の未確認 2 点、V10 の未確認、V12(c) の補足を扱う。

## Context

G-001(戦闘の単調さ)。D-008 により、Build は変更内容を正確に書いた時点で完了する。実コードの変更、ビルド、テスト、動作確認は行っていない。以後の Verify 以降は、この記述からシミュレーターが作る模擬ビルドに基づく。実機の証拠ではない。

Handoff 30 では、V1〜V12 のうち fail はなかった。V7 と V10 の一部が記述から確認できず、仕様との食い違い F-1 が 1 件あった。

## Findings

### 0. 確認結果(Handoff 31 の Open questions への答え)

1. **F-1**: 仕様 §3.3 の文面は曖昧ではない。「前回の Recovery が終わってから 2.5 s 以上」で、仕様に合わせて直す。**Handoff 28 の 2.2 の条件 1 は、すでに「前回の Recovery が終わってから」と書いていた。** 模擬ビルド 0.4 が「突進が終わってから」と書いた理由は、変更内容の記述からは分からない。以下の修正版では、起点を Recovery の終了(Chase に戻った時点)と明記する。「Charge の終了ではない」と書き、数値の例も添える。確認のため、遷移ログに Recovery の終了時刻を足す(2.4)。
2. **遠い角が同距離のとき**: 仕様 §4.1 と D-005 に定義がある。距離は中心間で比べ、同じ距離なら FL を選ぶ。Handoff 28 は「同じ距離なら FL」と書いていたが、「中心間」と座標の取り方がなかった。修正版に明記する。
3. **Grub の速度**: 仕様 §4.3 の数値は 2.0 / 2.0 / 2.2 / 2.2 / 2.4(部屋 1〜5)。Handoff 28 の部屋表にはこの数値がすでにあった。模擬ビルドが数値を落とした理由は分からない。修正版では、部屋ごとの速度を表の外にも列挙し、どの敵に適用するかを書く。
4. **V10**: 変更しない数値を、修正版に列挙する(2.2 の末尾)。
5. **V12(c) の補足**: 同じ波の複数スロットの待ちが、波を出すと決めた時点から同時に始まる、という 1 文を足す。仕様 §4.1 と D-009 に矛盾しない。

### A. 修正後の変更内容(2.1〜2.4 の全体)

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

**Grub 速度の数値(Chase で歩く速さ)**:
- 部屋 1: 2.0 タイル/s。
- 部屋 2: 2.0 タイル/s。
- 部屋 3: 2.2 タイル/s。
- 部屋 4: 2.2 タイル/s。
- 部屋 5: 2.4 タイル/s。
- その部屋の通常型 Grub と突進型 Grub の Chase(歩き)に、同じ値を使う。突進の速度 8.0 タイル/s とは別の値で、Charge には使わない。Spitter は動かない。

合計は 部屋 1: 3 体、2: 4 体、3: 4 体、4: 5 体、5: 6 体。同時に存在する敵の最大は 部屋 1: 2、2: 3、3: 3、4: 3、5: 4。部屋は、全部の波が出現し、全部の敵が倒れたときに終わる(既存の終了条件はそのまま使う)。

**スポナーの動き**:
- 波 1 は部屋の開始時に出す(各スロットの出現位置の待ちは次項)。
- 波 2 以降は、「生きている敵が K 体以下」または「前の波の最後の敵の出現中が終わってから T s」の先に起きた方で出す。「生きている敵」には出現中の敵を含める。T の起点は、その波の最後の敵の出現中が終わった時点(出現位置の待ちがあれば、待ちが終わって出現中も終わった時点)である。
- **波の条件を調べ始める時点(D-009)**: 波 N の次の波(N+1)の K と T は、波 N の全員が出現中に入った時点から調べ始める。それより前は、K の判定も T の計測もしない。そのため、出現位置の待ちに入っている敵は「生きている敵」に数えず、出現中に入った時点から数える。
  - 全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波を出す。そうでなければ、K 体以下になるか T s たつかの先に起きた方で出す。T の起点は上のとおりで変わらない。
  - 待ちの敵がいない波では、出現を決めた時点が、そのまま調べ始める時点になる(従来どおり)。
- **出現位置の待ち**: スロットごとに、出現の時点でプレイヤーとスロット座標の距離(中心間)が 4 タイル未満なら待つ。距離が 4 タイル以上になるか、待ちが 2.0 s に達したら、そのスロットの敵が出現中に入る。待ちはスロットごとに別々に数える。**同じ波の複数のスロットの待ちは、波の出現を決めた時点から同時に始まる。**(仕様 §4.1、D-009。追加の規則ではない。)いったん待ちが終わったスロットは、プレイヤーが戻ってきても待ち直さない(仕様 §4.1 の既存の文面)。プレイヤーがスロットに重なっていても押し出さない。
- **「FL / FR のうち遠い方」(部屋 3 の波 2、部屋 5 の波 2)**: その波の出現を決める時点(出現位置の待ちを始める前)のプレイヤーの位置から、FL のスロット座標と FR のスロット座標までの距離を、**それぞれ中心間の距離**で比べ、遠い方を選ぶ。**2 つの距離が等しいときは FL を選ぶ**(仕様 §4.1、D-005)。選んだあと、待ちの間にプレイヤーが動いても選び直さない。同じ波で FL か FR が別の敵のスロットとして指定されている場合は、この規則の対象外(固定のスロットが優先)。
- **突進スイッチ**: スポナーが敵を生成する 1 か所で、スイッチがオフなら `grub_charger` を `grub`(通常型)に置き換える。敵の数、波、スロット、K/T は変わらない。スイッチがオフでも、尾根の重ね絵など突進の見た目は何も付かない。部屋 1、3 には突進型がいないので、スイッチは効かない。

#### 2.2 敵コントローラ(共通)

**出現中(Spawning)**: 全種類の敵に追加する。長さ 0.8 s。この間は、動かない、行動しない、ダメージを与えない、プレイヤーの攻撃のダメージも怯みも受けない。終わると通常の状態(Chase)に入る。Spitter の最初の 1 発は出現中の終了から 1.0 s 後。以降は部屋ごとの間隔。

**Spitter の弾**: 速度 4.0 タイル/s、ダメージ 1 ハート。撃った瞬間のプレイヤーの位置へ直進(先読みなし)。壁で消え、敵の体を通り抜けて敵にダメージを与えない。弾の仕組みは作り直さない。Spitter 自身の怯みは既存のまま(0.2 s)。

**`grub_charger`(突進型)**: Grub のデータ(HP 2、Chase の速度は部屋の Grub 速度)に突進の数値を足したもの。別のコントローラは作らない。状態は Spawning、Chase(既存)、Windup、Charge、Recovery。通常型 Grub と同じ Chase、噛みつき、怯みの既存のルーチンを使う。

| 状態 | 長さ | 動き | 接触ダメージ | 怯み・ノックバック |
|---|---|---|---|---|
| Chase | 条件まで | 部屋の Grub 速度で歩く(既存の移動) | あり(既存の噛みつき、1 ハート) | 既存(0.2 s) |
| Windup | 0.7 s | その場で停止、歩行アニメーションも止める | なし | なし |
| Charge | 7.0 タイル進むか壁まで | 固定した方向へ 8.0 タイル/s で直進 | 突進ごとに 1 回まで(下記) | なし |
| Recovery | 0.8 s | その場で停止 | なし | なし |

**Chase → Windup の条件**(Chase の各更新で調べる。すべて満たすとき):
1. 次の 2 つの待ち時間が両方たっている。
   - (a) 出現中が終わってから 1.5 s 以上。
   - (b) **前回の Recovery が終わってから 2.5 s 以上。** 起点は、前回の Recovery が終わって Chase に戻った時点である。**前回の Charge が終わった時点ではない。**Recovery の 0.8 s は 2.5 s に含めない。例: Charge が時刻 t で終わると、Recovery は t から t+0.8 まで。次の Windup が始まれるのは、早くても t+0.8+2.5 = t+3.3 以降。まだ Recovery を一度も経ていない Grub は、(b) を満たしているとみなす。
2. プレイヤーとの距離(中心間)が 3.0〜6.0 タイル。
3. この Grub が `grub_charger` である(スイッチがオフなら生成されない)。
4. 生きている他の `grub_charger` が Windup または Charge にいない。Windup に入る瞬間に、生きている敵を調べて導く。保存する状態(トークン)は作らない。

Chase 中の怯みでこれらの待ち時間は巻き戻さない(起点は出現中の終了と前回の Recovery の終了で、怯みは影響しない)。

**Windup**: 入る瞬間のプレイヤーの中心へ向かう単位ベクトルを突進方向として固定する(距離が 3.0 タイル以上なので零ベクトルにならない)。その後プレイヤーが動いても変えない。0.7 s たつと Charge に入る(余りは持ち越す)。

**Charge**: 毎更新 8.0 × delta の距離を固定方向へ進む。通算 7.0 タイルに達するか、既存の移動処理が壁で止めたら終わり、すぐ Recovery に入る(壁に当たったときの特別な処理はない)。7.0 タイルを超えた分は、時間に直して(超過距離 ÷ 8.0)Recovery の経過時間に持ち越す。他の敵の体は通り抜け、ダメージを与えない。

**Recovery**: 0.8 s たつと Chase に戻る。この戻った時点が、上の条件 1(b) の起点になる。

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

**プレイヤー側の数値は変更していない(V10)**: この変更は、次のプレイヤー側の数値とコードに一切手を入れない。値は仕様 §1 のまま、既存の実装のままである。
- 攻撃: ダメージ 1、回復 0.35 s。
- ダッシュ: 0.25 s で 4 タイル、ダッシュ中はずっと無敵、クールダウン 0.6 s、ダッシュ中に押した攻撃はダッシュ終了時に出る。
- 被弾: 1 ハート。硬直 0.3 s(入力不可)、被弾から 0.8 s 後まで無敵。
- 無敵のフラグとその 2 つのタイマー(ダッシュの 0.25 s、被弾の 0.8 s)のコードは変えない。変更するのは、新しい突進が問い合わせ関数でフラグを読むことだけ。
- プレイヤーの移動速度、攻撃の届く距離、判定の大きさも変えない。新しい入力ボタンは足さない。

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
- **今回足したログ項目**: 突進型の Recovery の終了時刻(Chase に戻った時刻)。次の Windup の開始時刻との差が 2.5 s 以上であることを、ログから読めるようにするため。

### B. Handoff 28 との差分

1. **2.2 Chase → Windup の条件 1**: 起点を「前回の Recovery が終わって Chase に戻った時点」と明記した。「Charge の終了ではない」「Recovery の 0.8 s は 2.5 s に含めない」を追記し、数値の例(t+3.3 以降)を足した。Handoff 28 の文面も Recovery 終了後だったので、数値は変わらない。文面を具体的にしただけ(F-1)。
2. **2.1 Grub 速度**: 部屋 1〜5 の数値(2.0 / 2.0 / 2.2 / 2.2 / 2.4)を表のほかに列挙した。通常型と突進型の Chase の速度に使い、Charge の 8.0 とは別と書いた(V7 未確認 1)。2.2 の Chase の動きの欄にも「部屋の Grub 速度」と書いた。
3. **2.1「FL / FR のうち遠い方」**: 距離を「それぞれ中心間」で比べる、「2 つの距離が等しいときは FL」と明記した(V7 未確認 2)。仕様 §4.1、D-005 と同じ内容で、規則の追加ではない。
4. **2.1 出現位置の待ち**: 「同じ波の複数のスロットの待ちは、波の出現を決めた時点から同時に始まる」を独立した 1 文にして強調した(V12(c) の補足)。Handoff 28 にも同じ内容が含まれていた。
5. **2.2 末尾**: 「プレイヤー側の数値は変更していない」の節を新設した。攻撃の回復 0.35 s、ダッシュの 0.25 s・4 タイル・クールダウン 0.6 s、被弾の硬直 0.3 s・無敵 0.8 s、無敵フラグと 2 つのタイマーのコードに触れないことを列挙した(V10)。Handoff 28 は「プレイヤー側の数値やキットの変更は含めない」とだけ書いていた。
6. **2.4 開発ログ**: Recovery の終了時刻を足した(F-1 を確認しやすくするため)。
7. 変更なし: 2.3 の見た目のすべて。波、K/T、構成、接触の定義、怯みの規則。欠陥 D の扱い(触れない、原因を推測しない)。

### C. 模擬上の前提が残る項目(Handoff 17 の番号。Handoff 28 から変更なし)

実コードで確認済みではない。`sim/repo-notes.md` にはスポナー、部屋、波、出現位置、出現中の記述がない。

| # | 項目 | 結果 |
|---|---|---|
| 1 | 部屋データ、スポナー、波(敵の一覧で数える、スロットごとの待ちタイマー、全員が出現中に入った判定を 1 か所に置く) | 模擬上の前提 |
| 2 | 部屋のコードと敵コントローラの分離、部屋の終了条件と波の結合の強さ | 模擬上の前提 |
| 3 | 接触の判定形状と大きさ、レーン幅の元の値 | 模擬上の前提 |
| 4 | Spitter の弾(壁で消える、敵を通り抜ける) | 模擬上の前提 |
| 5 | 視覚の仕組み(必須要素 1〜6 が使える、敵の HP 表示がない、粒子を新規に足す。レーンの赤橙と弾・ランタンの色の近さは未確認) | 模擬上の前提 |
| 7 | 既存の敵の他のタイマー(噛みつきの間隔など)が delta で進んでいるか | 一部確認 / 一部模擬上の前提(delta、30/60 FPS、Flinch 0.2 s、無敵 0.25 s と 0.8 s は `sim/repo-notes.md` で確認) |

- 項目 6(接触結果の通知)は前提ではなく、この変更で足すもの。
- 前提が外れた場合の戻し先は、Handoff 17 と D-007 の 2 のとおり。
- スロット座標の実数値は不明のまま。各部屋で仕様の意味(奥、左右の側面、奥の左右の隅)に対応する位置にあるとして扱う。「遠い方」は、この座標の中心間距離で比べる。

### D. 実装していない・確認していないこと

- コードの変更、ビルド、テストの作成と実行は行っていない(D-008)。この文書は変更内容の記述だけである。
- 実機のゲームパッドの操作感、0.7 s の予告を読んでダッシュまで入力できるか、暗い床や小さい画面での読み取り(H1〜H4)は確認していない。
- 欠陥 D(被弾直後のダッシュ中のダメージ)には触れておらず、原因は推測していない。規則は `game-designer` が決める事項で、この Step では変更していない。
- 2 体の突進型が同じ更新で Windup の条件を満たす場合の順序は、既存の敵の更新順で決まる。仕様に規則がなく、この変更も規則を足さない。V5 には影響しない。
- 音、新しい入力ボタン、Spitter の変化、新しい敵は含めない。
- 仕様の欠落や矛盾は見つからなかった。`outcome: question` にする必要はない。

## Decisions already made

- D-001: 攻撃とダッシュのみ。新ボタンなし。
- D-004: 技術方針(共通コントローラへの状態追加など)。
- D-005: 怯み、接触の解決、「遠い方」(同距離は FL)。
- D-007: 前提の台帳。確認できない項目は「模擬上の前提」と明記する。
- D-008: Build は変更内容を正確に書いた時点で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- すべての結果は模擬ビルドに基づく(D-008)。実機の証拠ではない。
- 仕様と数値は変えていない。新しい入力ボタンなし。プレイヤー側の数値は変えていない。
- 欠陥 D の原因は推測しない。

## Open questions

- なし。Handoff 31 の 3 つの問いには、上の「0. 確認結果」で答えた。
- 再検証で、模擬ビルドが再び突進の再開始の起点を Charge の終了と書いた場合は、記述が仕様と一致していても起きたことになる。その場合の原因は、変更内容の記述からは判断できない。Studio が扱いを決める。

## Expected output

Studio は、A(修正後の 2.1〜2.4)と B(差分)を使って Verify の Handoff を組み直し、`qa` に F-1、V7、V10、V12(c) の再検証を依頼する。2.3 は `art-director` 向け。`qa` には Sender assessment を渡さない。

## Sender assessment

- 確信度: 数値と規則はすべて `design/combat.md` §1、§3.3、§4.1、§4.3 と D-005、D-009 から写した。仕様との対応は高い。
- F-1 について: Handoff 28 と `sim/repo-notes.md` はともに「Recovery が終わってから」と書いていた。模擬ビルドの食い違いが記述の曖昧さによるものとは言い切れない。文面を具体的にして再検証に出すのが、この Step でできる範囲である。
- Grub 速度についても同様で、Handoff 28 の表には数値があった。列挙を足したのは確認しやすくするためで、数値は変えていない。
- 低いのは、台帳 1〜5 の模擬上の前提と、見た目の細部(レーン長の求め方、使用済み表示の描き方)。変更はない。
- 範囲外は広げていない。欠陥 D の原因の推測は書いていない。

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md、sim/build-0.4.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/31-studio-to-gameplay-engineer.md
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END
