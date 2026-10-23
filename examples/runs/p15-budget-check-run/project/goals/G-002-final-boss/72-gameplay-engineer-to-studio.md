---
kind: handoff
goal: G-002
seq: 72
from: gameplay-engineer
to: studio
stage: Build
outcome: partial
---
# 72: gameplay-engineer → studio — E1公開境界prototype保存、実経路接続は継続

## Task

同Roleの直列継続でE1を完了する。公開境界prototypeを実dodgerへ接続し、記憶の寿命、全判断ログ、全分岐試験と表示証拠を揃える。E2はまだ開かない。

## Context

71と68§4を受領した。今回保存するのは公開観測・純粋判断のprototypeと3試験であり、実際のボスbot修正完了ではない。60のfailを維持する。新しい仕様質問や供給不足はない。

## Findings

### 保存変更と挙動

変更はrepo/bots.py、repo/tests/test_bots_boss.pyのみ。packetの未保存prototypeを基に、独立したBossObservation、BossMemory、BossChoice、observe_boss、choose_bossと3試験を保存する。

プレイヤー表示、戦闘、実dodger、camper、walker、独立1〜4の実行方針は変更していない。prototypeは未接続で、判断候補の実用性や攻略可能性も未検証である。ゲーム仕様の新しい挙動を追加しない。

### 公開フィールド対応

| 入力 | 根拠 | 制限 |
|---|---|---|
| t | 公開driverのroom time | 判断履歴の出典時刻 |
| x,y,boss_x,boss_y | play.spritesと既存公開Viewの位置観測 | 文字セルだけから連続座標を復元した証明ではない |
| phase,attack | Output.emitのboss status、next | HPは生存対象の選択だけに使用 |
| aim,warning_left | warningのlocked方向、残時間 | warning以外はNone。activeの値は読み取らない |
| shots | 公開spriteの弾位置 | velocity、age、ID、source、lifetimeなし |
| memory.lane,attack,warning_time | 過去warning観測 | active中は全固定経路を保持。recovery/approachで解除 |

固定危険幅、射程、盤面寸法、方向は仕様値・既存定数を使う。0.3 tileの余裕、弾近傍1.1 tile、移動先1.5 tile、接近閾値1.1 tileはprototypeの方針値であり製品パラメータではない。

### 監査範囲と未解消経路

choose_bossは観測と記憶だけを受け、Game/Enemyやpressを受け取らない。参照補助はmath.hypot、_toward、DIRECTIONS、ROOM_W/Hのみで、内部状態へ戻らない。warningから固定経路を作り、activeでは短縮しない。履歴不足はmissing-warning-historyを返し、最大半径で扱う。候補、壁除外、選択、予定ボタンをBossChoiceに返す。

ただし実dodgerは従来経路のままである。_dangersのactive phase_left参照、_threat、_escape、_face_and_swing等を通る旧判断は未修正。新境界の不変試験は旧経路の不適合を解消しない。

prototypeにはdash判断がなく、warning残時間も保持するだけで選択には使わない。stun省略、判断番号/grid、発行済みボタン、入場/retry初期化との接続はない。候補の全件列挙ではなく、最初に採択した候補で返る。これらを全分岐監査済みとしない。

### 試験追加

追加IDは以下の3件。既存試験のassert・対象は削減していない。

- test_bots_boss.PublicBoundaryPrototypeTest.test_active_internal_values_do_not_cross_boundary：
  両攻撃でactive残時間0.001/99、struck/spent、非表示aimを変えても観測と選択が一致。activeのaim/warning_leftはNone。
- test_bots_boss.PublicBoundaryPrototypeTest.test_warning_memory_active_and_recovery：
  chargeのwarning履歴保持、activeの全経路判断、recovery解除、履歴なしactiveの不足表示をassert。
- test_bots_boss.PublicBoundaryPrototypeTest.test_slots_only_input_and_visible_branches：
  slots入力、approach/swipe/hold/escape、距離0、下壁除外と上移動、近傍弾をassert。

不足は両FPSの実経路、短射の遷移全条件、左右・上壁、端点、距離境界、dash待ち、stun、入場/retry、警告履歴なし範囲の全方向、許可外属性を読むと失敗するadapter fixture、全選択分岐ごとの内部値不変である。slotsだけで全呼出経路の許可外参照禁止を証明しない。

### 収録実行と識別

packetのRound 1は、未保存prototypeを使った固定コマンド
`python3 -m unittest discover -s tests`、Exit 0、157 tests、source_id 5c62a1c7e18eを報告している。

今回保存したprototypeはコメント等も整理しているため、このsource_idを最終保存集合の識別として流用しない。最終集合の識別とsuite結果はruntime Build checkで照合する。識別対象は6ソースとtests/*.pyの13ファイル、計19ファイル。設計資料とHandoffは対象外。

Round 1の棚卸しは13ファイル・157IDを全表示しENDあり。旧154から上記3件増加。SPLIT_C出力は3865文字切断されており、切断部分は未確認。表示された旧実dodgerのボス成績もE3の新測定ではない。

状態・判断本文のemit_rowsアダプタ、窓helperの外側への確認本文再表示は未実装。今回その本文を収録したとの主張はしない。repo/tests/test_g002_evidence.pyとtest_split_c.pyは変更していない。

### 継続手順と配布台帳

次のE1継続では実装前に境界接続の失敗試験を追加し、実dodgerが内部Gameを純粋判断へ渡さないことを検査する。Brain等に記憶を所有させ、部屋入場・retryで初期化する。直接dodger呼出と通常run、_Proxyによる入力捕捉の互換も試験する。

判断番号、grid、時刻、公開入力、記憶出典、候補・除外、選択・発行ボタン、stun省略を出す。内部ログ観測は選択後に別経路で取得する。既存印字はassertを保ったまま対象別に抑制し、概ね12000字以内でemit_rowsのBEGIN/ENDと欠落範囲を確認する。

追加3IDは既存F04内であり、新ファイルは0。71の台帳に従いQ1とQ4へ更新本文を配布する。Q1が公開境界の主担当。13ファイルの未割当0は維持するが、配布済みは基準充足を意味しない。70の番号は追加によりずれるため、対応は完全IDで追跡する。

70の未解決事項は保持する。E2接触診断、E3四条件、E4未丸め/half-upと共有正本の完全対応、E5公開再生再生成、長時間観測、独立QA以降には着手していない。D-024の歴史的確認不能一覧も解消していない。

### Sender assessment

prototypeの境界形状と限定した不変assertは準備できたが、実判断経路は旧実装でありE1未完了と評価する。収録157件成功はこの限定的な自己確認であり、独立QA、公開情報限定botの完成、ボス四条件測定、Goal達成の証拠ではない。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較を維持。
- D-021/D-023：Studio内テキスト検証と供給上限内の直列継続。
- D-022：表示・弾・長時間観測契約は変更しない。
- D-024：現行検証、記録比較、歴史的確認不能を分離。
- 68：E1完了後、Studioが別HandoffでE2を開く。

## Constraints

製品仕様、難度、戦闘パラメータ、表示、秒数ゲート、Goal範囲を変更しない。実装者の自己確認で60のfailを上書きしない。未表示や切断をpassにしない。実機、変更前ビルド、全文保存先を再要求しない。

## Open questions

新しい仕様質問はない。残作業は既知のE1実装・試験・表示であり、同Roleへ継続する。

## Expected output

StudioはE1 partialとして同Roleの直列継続をルートする。実経路接続、全判断分岐の公開対応、記憶初期化、内部差不変、必要本文と最終source識別を揃えてからE1完了を確認する。E2〜E5および独立QAの完了とは区別する。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.1 s).

```text
ublic-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.332541857031174, "source_id": "8fe9bcc21225"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "8fe9bcc21225", "trial_count_per_room_fps": 1}
.............................................................................................................................................................
----------------------------------------------------------------------
Ran 157 tests in 2.963s

OK
```

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/bots.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting handoff: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
