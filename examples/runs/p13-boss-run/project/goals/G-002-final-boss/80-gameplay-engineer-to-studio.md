---
kind: handoff
goal: G-002
seq: 80
from: gameplay-engineer
to: studio
stage: Route
outcome: partial
---
# 80: gameplay-engineer → studio — 突進被弾の誤診断を修正・保存、E1接続は未完了

## Task

68のE1診断準備として、ボス突進の被弾ログがshot診断へ流れる問題を修正し、両FPSの制御接触試験と確認本文を保存する。実dodger接続・被弾差の原因確定・実経路監査は同Roleの継続へ返す。

## Context

79からD-025・D-026の上限付き継続を受領した。今回packetの出発点はsha `61492279ed13`。76のsource `e99408d647c7`・160 tests成功を現行確認として流用しない。

Inputsには今回Round 1の未保存案と実行結果がある。その案の2ファイル変更を本成果へ保存する。E1完了、E2開始、独立QA判定、Goal達成は宣言しない。

## Findings

### 今回の単位と変更

今回の単位は、76が挙げた互換診断単位に先立つ「被弾源を取り違えるログの修正」である。68のE2で必要になる診断分離の一部にも対応するが、E2全体を実施したものではない。

変更ファイル：

- `repo/bots.py`：`_hurt_lines`にsource `boss`専用分岐を追加。突進後のボス位置、プレイヤーとの移動後距離、struck・spentを出す。
- `repo/tests/test_bots_boss.py`：`AContactDiagnosticTest.test_charge_hurt_log_is_not_a_shot_diagnostic`を追加。

プレイヤーが観測する戦闘・player viewの変更はない。botログの突進被弾行だけが変わる。HP、移動、攻撃、時間、難度、入力、公開表示契約は変更していない。

実dodgerは旧経路のまま。`choose_boss`はprototypeであり、公開境界へ接続していない。旧`_dangers`のactive chargeは引き続き内部`phase_left`を読む。CLIの「displayed boss fields only」という既存説明も、実経路の適合証拠にはならない。

### 実行・証拠の識別

InputsのRound 1：

```text
python3 -m unittest discover -s tests
source_id: fc07c7db6383
exit: 0
tests: 161
unittest elapsed: 3.502 s
executor elapsed: 3.6 s
```

本成果はRound 1の未保存案と同じ変更を保存する。最終保存集合の識別と実行結果は、このHandoffへ付加されるruntime Build checkで照合する。上記識別を最終保存後に再算出済みとはしない。

識別対象は既存の6ソースと`tests/*.py`の13ファイル、計19ファイル。Handoff・設計資料・manualは対象外。

証拠ID：

`E1/charge-hurt-log/current-controlled-fixture`

BEGIN、連番001・002、ENDを収録本文で確認できる。総2行、表示2行、未表示0行。条件は独立5番の制御fixture、開始3 hearts、プレイヤー(8,4)、ボス(8.5,4)、active charge、aim(-1,0)、残時間0.3秒。各FPSで1 frame進めた後の診断であり、通常到達や実bot方針の証拠ではない。

| FPS | frame | 移動後ボス位置 | 移動後距離 | hearts | struck | spent |
|---|---:|---|---:|---:|---|---|
| 30 | 1 | (8.233333,4) | 0.233333333 | 2 | true | false |
| 60 | 1 | (8.366667,4) | 0.366666667 | 2 | true | false |

試験はログ1行、source boss、boss charge位置・移動後距離の存在、shot文字列の不在をassertする。ログ取得前後で位置・hearts・events・接触フラグが不変であることも検査する。内部状態は戦闘後の診断専用であり、判断入力へ返していない。

Round 1の棚卸しは13ファイル・161IDのBEGIN/ENDまで表示された。一方、後続出力には6731文字の切断がある。`E1/input-replay`の必要本文は本収録から確認できない。suite成功を生成・再生一致の表示証拠に置き換えない。切断されたSPLIT_C_BOSS等も補完しない。

### QA配布台帳の更新

70・76の13ファイル割当を維持する。新規ファイル0、変更ファイル2、追加ID1、未割当ファイル0。完全IDを使用し、今回の棚卸しで変わった連番を過去の番号と混同しない。

追加ID：

`test_bots_boss.AContactDiagnosticTest.test_charge_hurt_log_is_not_a_shot_diagnostic`

| QA | 今回の更新配布 |
|---|---|
| Q1 | bots.py、test_bots_boss.py。突進被弾ログと実公開境界が別対象であることを照合 |
| Q2 | bots.py、test_bots_boss.pyを追加配布。制御接触の観測範囲を照合 |
| Q4 | 既存割当のtest_bots_boss.py更新本文。player表示変更なしという実装範囲を照合 |
| Q5・Q6 | 既存割当に加えbots.py更新本文。共有bot経路の変更範囲を照合 |

Q3の既存割当は変更しない。全13件の基礎割当は76の台帳を継承する。配布予定と独立検証済みは区別する。

### 残作業と依存

E1は未完了。次の同Role単位は実接続であり、接続せずprototype試験だけを追加して完了とはしない。

1. 実dodgerのボス分岐を、旧共有補助経路より前に公開観測・判断境界へ接続する。直接呼出、play_room、_Proxy、play_runで記憶所有を統一し、入場・retryで初期化する。
2. 接続集合で生成・公開再生の全フレーム対照を実行し、必要本文を短い出力へ分割する。pause/retryあり・なしを分離して被弾差の発生箇所を確定する。既存hits0 assertを緩和しない。
3. 実接続経路の許可外読取guard、内部active値差に対する判断不変、共有補助関数への迂回禁止を検査する。
4. warning→active→recovery、距離0、壁・端点、dash待ち、stun、履歴不足、入場・retryの全対象を検査する。
5. 全判断の番号・grid・公開入力・記憶由来・候補・除外理由・選択・実発行入力と、stun省略を記録する。全件検査と表示窓を分離する。

今回の試験は通常命中1 frameだけ。無傷接触、保護前後、消費前後、非接触距離、次攻撃を含むE2診断は残る。E3四条件再測定、E4保持回帰・未丸めhalf-up記録比較、E5公開入力再生成・通常到達・player対照、Q1〜Q6、限定Art Verify、独立Play、Designer判断、Reviewも未実施である。

### Sender assessment

誤ったshot補助文の原因は、`_hurt_lines`がgrub以外のhurtを全てshotとして扱っていたことにある。source bossを分離する修正はRound 1の両FPS fixtureで確認できた。

これは接続案の被弾差の根因ではない。実dodger接続とその原因確定は未成立である。既存計画が実行不能だと示す新事実はなく、今回の限定成果をpartialとして保存する。自己試験結果を独立QAや体験判定へ拡張しない。

## Decisions already made

- D-025：実公開境界、接触診断、再測定、保持回帰、通常公開再生、独立評価を維持。重複整形・存在しない資料の探索は省く。
- D-026：累計83 operationsから40追加、budget 123。完成保証や無制限継続ではない。
- D-024：現行検証・現行内対照・記録比較・歴史的確認不能を分離する。
- 68：E1完了確認後にE2以降を直列で進める。

## Constraints

仕様、戦闘パラメータ、難度、秒数ゲート、Goal範囲を変更しない。60のfailを上書きしない。旧bot時間を対応後基線やプレイヤー時間に使用しない。

未表示、切断、未実行、歴史的確認不能を成功扱いしない。追加環境・変更前ビルド・全文保存先を要求しない。独立QA、限定Art Verify、独立Play、Designer判断、Reviewを省略しない。

## Open questions

新たな仕様質問・Ownerへの供給質問はない。

技術上の未確定事項は、公開境界接続後の被弾差が生成・再生差か、制御列の影響か、方針と実接触の差かである。今回のログ修正では確定していない。

## Expected output

Studioは本変更と証拠範囲を保存し、E1をpartialとして同Roleへ継続ルートする。次の単位は実公開境界接続と、その集合での互換診断・必要本文の確認とする。

E1完了、E2開始、再測定済み、QA合格として扱わない。後続QAへは担当ソース・試験本文・再現条件を渡し、Sender assessmentを判定根拠として渡さない。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.6 s).

```text
-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3302503449958749, "source_id": "fc07c7db6383"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "fc07c7db6383", "trial_count_per_room_fps": 1}
.................................................................................................................................................................
----------------------------------------------------------------------
Ran 161 tests in 3.527s

OK
```

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: repo/bots.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Supporting handoff: goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
- Decisions: decisions/D-025-g002-minimum-remaining-scope.md
- Decisions: decisions/D-026-owner-extends-g002-budget.md
- Previous handoff: goals/G-002-final-boss/79-studio-to-gameplay-engineer.md
