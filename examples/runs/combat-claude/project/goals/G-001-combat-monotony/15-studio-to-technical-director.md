---
kind: handoff
goal: G-001
seq: 15
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 15: studio → technical-director — Build の最初の調査(T0)を実施できなかった。進め方を再確認する

## Task

Build(`gameplay-engineer`)が、D-004 の前提を確かめる最初の調査(T0)を実施できず、実装に入らずに返してきた。T0 を実施できない状況で Build をどう進めるか(または進められないか)を、技術方針として決めてほしい。あわせて、Build が返した 2 つの技術的な問い(要素 9、必須の視覚要素)に答えてほしい。

## Context

Goal G-001「戦闘の単調さの改善」。方向は D-002、規則は D-003 と D-005、技術方針は D-004、突進の予告の見た目は D-006 で決まっている。Build の Handoff 13 は、最初に T0(既存の仕組みの調査)を行い、前提が崩れたら実装に入らず返す、と指示していた。

`gameplay-engineer` は T0 を完了できなかった。理由は、その実行に、ゲームのコード、動かせるビルド、テストの実行手段がなく、使えたのは仕様、Decision、`sim/repo-notes.md`、`sim/build-0.3.md` だけだったため。`project.md` は `repository: none`(サンプルで、ビルドは `sim/` で模擬)としている。D-004 も「`sim/` の記述に基づく見積もりで、コードは読んでいない」と書いており、同じ状況が続いている。実装、テスト、ビルドは一切行われていない。

Studio は、リポジトリの提供や別の担当による T0 は、同じ入力では同じ結果になり、Studio が process として用意できるものではないと判断した。技術方針と順序の決定は `technical-director` の権限なので、ここに回す。

## Findings

### Build が `sim/repo-notes.md` から確認できた事実(Handoff 14 の報告)

- 敵は 1 つの共通コントローラを共有する。状態は Idle、Chase、Attack。種別ごとの違いはデータ(速度、HP、攻撃の種類)と小さな種別ごとの攻撃ルーチン。D-004 の「状態の追加」の前提と矛盾しない。
- 被弾した敵は、0.2 s の Flinch に入る。Attack を含め実行中の行動を中断し、Chase に戻る。D-005(突進型の Windup、Charge、Recovery では怯まない)は、状態で分岐する必要がある。
- プレイヤーの攻撃は、前方の短い弧の判定で、敵との重なりでダメージを与える。
- プレイヤーの無敵は、オン/オフの 1 つのフラグ。ダッシュは 0.25 s のタイマーを、被弾は被弾から 0.8 s 後に終わるタイマーを開始する。どちらのタイマーも、終わるとフラグをオフにする。つまり、2 つのタイマーが 1 つのフラグを共有している。D-004 の無敵の問い合わせ関数は、この 1 つのフラグを読む形で作れる。
- 移動は単純なステアリングで、壁で止まる。
- 更新は可変 delta で、30/60 FPS をサポートしている。D-004 の delta 上限 0.05 s を入れる余地はある。
- 敵とプレイヤーのテスト、無敵のテストは無い。テストの枠組みの有無は不明。

### 確認できなかった項目(T0 の確認項目のうち、`sim/repo-notes.md` に書かれていないもの)

1. 部屋データの形、スポナー、「3〜6 体を最初に全部出す」前提かどうか(波に対応できるか)。
2. 部屋のコードと敵のコントローラが別モジュールか(T2 と T3 を並列にする条件)。
3. 敵とプレイヤーの接触の判定形状(円か矩形か)。スイープ判定の方法と、レーン幅を接触判定の範囲に合わせる元の値。
4. Spitter の弾が、壁で消え、敵を通り抜ける扱いか。弾の衝突の仕組み。
5. 視覚の仕組み: 地面層に半透明の帯を描けるか。スプライトの色変調と変形(拡大縮小、描画ずらし)。重ね絵。敵の HP 表示と被弾の白いフラッシュの有無。既存の出現演出と粒子。Spitter の弾の色とランタンの色(レーンの赤橙との差)。
6. 接触の結果(無敵で抜けた / 被弾)を見た目へ出す口を作れるか(視覚仕様の要素 9)。
7. 敵の挙動を経過時間で進めているか(仕様 §9 の項目 6)。可変 delta という記述から時間ベースらしい、という程度。

### Build が止めた判断

- 確認できないままコードを前提に実装すると、D-004 の見積もりの外れを見落とす危険があるため、実装に入らなかった。
- 仕様の曖昧さ・矛盾は見つけていない。`game-designer` への質問は無い。

## Decisions already made

- D-001: 攻撃とダッシュのみ。新ボタンは Owner 承認なしでは不可。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進の 1 つだけ。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。部屋は突進スイッチで外せる。
- D-004: 技術方針(共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ)。`sim/` に基づく見積もりで、T0 で確認する前提。
- D-005: 突進型は 3 状態で怯まない。接触は突進ごとに最初の重なりで 1 回だけ解決。「遠い方」は出現を決める時点で選ぶ。
- D-006: 突進の予告は「地面のレーン + 熾火の点灯 + 沈み込み」。赤橙は害になる状態だけに使う。

## Constraints

- 戦闘の規則・数値・仕様、D-001〜D-006 は、この Plan では変えない。変更が必要と分かった場合は、Decide(`game-director`)または Design(`game-designer`)に回すための Handoff を書く(自分で決めない)。
- 欠陥 D(被弾直後のダッシュ中のダメージの疑い)は今回の Build の範囲外で、`qa` の再現(2b)の結果待ち。この Plan で原因を決めない。
- 新しい入力ボタンは足さない。開発用補助は開発ビルド限定(D-004)。
- 小さなチーム。既存の仕組みを再利用する案を優先する。30/60 FPS の両方で正しく動くこと。

## Open questions

1. T0 を実施できる手段(コード、ビルド、テスト実行)がない状況で、Build をどう進めるか。選択肢の候補は次のとおり。ほかの案があれば、それを示してよい。
   - (a) T0 の未確認項目を、リスクつきの前提として明示し、前提が崩れる箇所を実装中に検出する手順を決めて、Build を進める。
   - (b) 未確認項目を先に仮定で埋めた計画を作り直し、Build の対象を縮める(例: 部屋と波を先に、見た目は縮小案など)。
   - (c) コードやリポジトリの提供が不可欠だと判断し、Owner に確認する。
2. 視覚仕様の要素 9(接触の結果の通知)が、D-004 の「見た目への口」に含まれるか。含まれず、追加も難しい場合の扱い(省く / 縮小案 / 技術方針の変更)。
3. 必須の視覚要素(Handoff 13 の 1〜6)が、既存の仕組みで実現できるか。確認できない前提のもとで、縮小案(`design/grub-charge-telegraph.md` §11)で足りるかの見立て。
4. 無敵フラグが 2 つのタイマーで共有されている点は、D-004 の問い合わせ関数の設計に影響するか。欠陥 D は別扱いのまま、問い合わせ関数が読む前提(1 つの真偽で答える)に見直しが要るかだけ答える。

## Expected output

次の 3 つのどれか。いずれも `to: studio` 宛て(Build の再開、Escalation、Verify の準備のため。Studio が次の Handoff を組む)。

1. Build を進められる場合: 更新した技術計画(T0 の扱い、未確認項目と前提、前提が崩れたときの戻し先、並列化の条件)と、Open questions 1〜4 への回答を Findings に書く。significant なら Decision(`make-decision`、`decisions/D-NNN-...md`)を記録する。
2. 仕様や方向の変更が要る場合: `outcome: question` で、どの Role(`game-designer` または `game-director`)に何を決めてもらうかを書いて返す。
3. Owner の判断が要る場合(リポジトリの提供、スコープ・リスクの受け入れなど、エスカレーションの条件に当たる場合): `prepare-owner-escalation` で Escalation(templates/escalation.md、`owner_language` は ja)を作る。選択肢、推奨、各選択肢の次の route を含める。

## Sender assessment

Studio の見立て: 実装者が推測でコードを書かずに返したのは妥当。T0 を実行できるのは、コードを読める環境だけで、この Goal の入力ではそれが得られない。そのため、技術方針の決定として扱うのが妥当と判断した。Escalation が必要かどうかは、`technical-director` がリスクの大きさを見て決める。Studio は結論を先取りしていない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md, studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md(frontmatter の repository、#constraints), sim/repo-notes.md, sim/build-0.3.md, design/combat.md, design/grub-charge-telegraph.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-005-flinch-contact-and-far-slot-rules.md, decisions/D-006-grub-charge-telegraph-visual.md
- Previous handoff: none(Handoff 14 は engineer の Sender assessment を含むため渡さない。必要な事実は Findings に抜き出した)
