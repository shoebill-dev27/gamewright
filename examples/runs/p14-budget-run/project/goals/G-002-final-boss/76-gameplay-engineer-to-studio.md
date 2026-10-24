---
kind: handoff
goal: G-002
seq: 76
from: gameplay-engineer
to: studio
stage: Route
outcome: partial
---
# 76: gameplay-engineer → studio — 再生互換診断を保存、E1の分割・再計画へ

## Task

E1連続partialの3回目としてTechnical Directorへ分割・再計画を戻す。公開境界の実接続、互換失敗の原因確定、記憶・全分岐・判断本文を完了単位へ分ける。E2以降は開かない。

## Context

75を受領した。保存済み出発点はsource b0770a4180c9、159 tests OK。72・74がE1 partialで、70のE0 partialは回数に含めない。60のfailを維持する。

packet内Round 1は未保存のtest_split_c.py案を実行したsource 9b4f6722e7df、160 tests OKである。実dodgerは旧経路のままであり、公開境界接続案の成功を意味しない。

## Findings

### 保存変更と挙動範囲

変更は次の2ファイル。製品・botの行動変更はない。

- repo/tests/test_split_c.py：test_generated_inputs_replay_without_controlsを追加。
- repo/tests/test_g002_evidence.py：窓helperの自己試験で捕捉・assertした本文を外側へ再表示する。

前者はpacketの未保存案を基に、比較状態へheading、facing、dash、cooldown、stun、攻撃recovery、保護、敵phase・timer・aim・接触消費状態を追加した。この内部観測は診断専用で、判断入力へ戻さない。今回の保存集合は9b4f6722e7dfと異なる。最終source_id・結果はruntime Build checkで識別する。

既存assert・既存対象集合は削除・緩和していない。未保存の接続案eddd95dd5926／189dbf689d7eは採用していない。

### 再生互換診断の再現とassert

追加完全ID：

test_split_c.SplitCTest.test_generated_inputs_replay_without_controls

両FPSについて、通常初期状態、開始3 hearts、mode run、limit 1200、driver-limit 1205で実施する。生成中は_Proxy.pressの全呼出を時刻・action・directionとして捕捉し、RunSession.step後の全フレームを記録する。生成側wonを要求する。

生成入力は小数12桁の時刻で公開構文へ変換し、play.read_scriptで解析する。入力件数・順序・ボタン一致、時刻差1e-9以内をassertする。再生はdriveでtimed inputsのみを使い、ライブbot・状態注入・pause・retryを使わない。全フレーム数と全記録状態の完全一致、再生clear、生成と再生のhurt件数一致をassertする。

出力列はfps、inputs、generated_frames、replayed_frames、first_difference、replay_hurts、generated_outcome、replay_outcome。FPSごとにemit_rowsで総1行・表示1行、BEGIN/END・列・除外を出す。first_differenceがあれば元集合のフレーム番号と両状態をassert前に出す。状態の位置とshot位置を含むが、接触直前後の実距離・消費専用列は未実装である。

この試験は同じ旧方針の生成・再生一致を切り分ける道具である。未保存接続案の被弾1の原因、公開境界適合、E5通常ラン受け入れの証明にはしない。

### 収録実行と表示の限界

固定コマンド：

```text
cd repo
python3 -m unittest discover -s tests
```

packet内Round 1はsource 9b4f6722e7df、160 tests OK。今回の比較項目追加前の集合である。INVENTORYは13ファイル・160IDを表示したが、後続には5335文字の切断がある。今回必要なEVIDENCE_BEGIN/ENDと診断行を収録本文で照合できず、生成・再生の具体的な一致本文は未確認とする。切断部分を推測で補わない。

今回新たな@run要求は出していない。最終集合の自己試験結果はruntime Build checkへ委ねる。予想discover数は保存済み159＋新規1＝160。件数成功で必要本文を代替しない。

識別対象はgame.py、session.py、play.py、run_driver.py、bots.py、source_id.pyとtests/*.pyの13ファイル、計19ファイル。Handoff・設計・manualは対象外。

### 公開フィールドと実経路監査の現状

prototypeの対応は維持する。

| 入力 | 公開対応 |
|---|---|
| t | room time |
| x,y,boss_x,boss_y | 既存sprites/Viewの連続位置観測 |
| phase,attack | Output.emitのboss status、next |
| aim,warning_left | warningのlocked方向・残時間 |
| shots | 実弾sprite位置 |
| lane,attack,warning_time | warning履歴 |

文字セルから連続座標を復元できたとはしない。

observe_bossとchoose_bossの限定監査は既存5IDが担当する。実dodgerは依然として_dangers→_threat→_escapeと_face_and_swing等の旧経路を使い、active chargeのphase_leftを読む。したがって公開情報限定は未成立である。直接呼出・_Proxy・play_room・play_runの実ボス判断を境界へ接続したとはしない。

warning記憶の実所有・寿命・入場/retry初期化、実経路の許可外参照禁止、両FPS・両攻撃の距離0・境界・端点・全壁・dash待ち・stun・履歴不足各方向、全判断番号・grid・公開入力・記憶由来・候補/除外・選択・実発行ボタンの統一記録は未完了。状態・判断の専用emit_rowsアダプタも残る。

### 窓helper確認本文

test_g002_evidence.EvidenceToolTest.test_bounded_selection_reports_missing_rangesは、3行中2番だけを表示し、total3/shown1、前後未表示各1、002 [2]、END、不正start拒否をassertする。今回、その捕捉本文をassert後に外側へ出すようにした。全件評価と表示窓の違いは維持する。この変更だけで判断列アダプタや出力欠落検査が完成したとはしない。

### 試験・QA配布台帳

13ファイルの割当は71のまま維持する。新規ファイル0、追加ID1、変更ファイル2。未割当ファイル0。既存159IDは維持する。

| QA | repo/tests/配下の配布ファイル |
|---|---|
| Q1 | test_bots_boss.py, test_g002_evidence.py, test_game.py, test_play_run_controls.py, test_split_c.py |
| Q2 | test_boss.py, test_boss_contract.py, test_boss_contract_details.py, test_d022_shots_and_note.py, test_g002_evidence.py |
| Q3 | test_boss_contract_details.py, test_g002_evidence.py, test_play_run_controls.py, test_run_driver.py, test_session.py, test_split_c.py, test_terminal.py |
| Q4 | test_bots_boss.py, test_d022_observation.py, test_d022_shots_and_note.py, test_g002_evidence.py, test_game.py, test_run_driver.py |
| Q5 | test_g002_evidence.py, test_game.py |
| Q6 | test_g002_evidence.py, test_game.py, test_split_c.py |

新規IDはQ1主担当、Q3・Q6にも配布する。変更したhelper試験はQ1〜Q6へ更新本文を配布する。既存追加5IDもQ1主担当・Q4への配布を保持する：

- test_bots_boss.PublicBoundaryPrototypeTest.test_active_internal_values_do_not_cross_boundary
- test_bots_boss.PublicBoundaryPrototypeTest.test_warning_memory_active_and_recovery
- test_bots_boss.PublicBoundaryPrototypeTest.test_slots_only_input_and_visible_branches
- test_bots_boss.PublicBoundaryAuditTest.test_all_escape_candidates_are_enumerated
- test_bots_boss.PublicBoundaryAuditTest.test_adapter_rejects_forbidden_attribute_reads

### 再計画に渡す実装単位と依存

1. 接続単位：実dodgerのボス分岐を公開観測・記憶へ接続し、所有を直接呼出・_Proxy・部屋入場/retryで統一する。旧1〜4方針を維持する。
2. 互換診断単位：接続後、今回の全フレーム対照で入力解析差とシミュレーション差を分ける。既存pause/retry試験でのみ差が出るなら、その制御前後と被弾フレームの接触条件へ絞る。既存hits0を弱めない。
3. 監査単位：接続済み全経路のguard、不変性、記憶・全分岐をassertする。接続と独立したprototype成功を代用しない。
4. 証拠単位：判断番号・grid・省略を統一し、状態/判断アダプタで全件検査と表示窓を分ける。既存長文印字との出力予算も整理する。

1が2・3・4の実経路成立条件であり、2の解消と3・4の充足までE1完了とはしない。今回は診断道具とhelper本文露出を保存したが、接続と原因確定は未成立である。

70の後続残作業を保持する。E2実接触・消費診断、E3四条件再測定、E4正本との完全対応・未丸めhalf-up記録比較、E5入力再生成・通常到達・player対照・旧未来入力破棄、長時間出力の不足、独立Q1〜Q6、歴史的確認不能の工程判断、Art Verify、独立Play、Designer判断、Reviewは未完了。

### Sender assessment

旧経路用の再生互換診断を具体化した。接続案の被弾差の根因は確定していない。未保存案の切断出力を接合せず、保存済み基線から変更した。E1は連続partial3回目として再計画を要する。自己試験成功が得られても独立QAやGoal達成を意味しない。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較。
- D-021・D-023：Studio内テキスト検証と確定供給上限を維持。
- D-022：表示・弾・長時間観測契約を維持。
- D-024：現行検証・現行内対照・記録比較・歴史的確認不能を分離。
- 68：E1完了確認後にE2を別Handoffで開く。

## Constraints

製品仕様・戦闘パラメータ・難度・秒数ゲート・表示契約・Goal範囲を変更しない。60のfail、切断・未表示、歴史的確認不能を自己確認で上書きしない。既存assertを弱めない。

## Open questions

新しい仕様質問・Ownerへの供給質問はない。Technical Directorには上記4単位の依存と供給上限に適合する分割を求める。被弾差の根因は未確定の技術課題として残す。

## Expected output

StudioはE1連続partial3回目としてTechnical Directorへ分割・再計画を戻す。完了部分と未成立条件を維持し、E2以降・独立QAを先行させない。同じ供給質問をOwnerへ戻さない。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.5 s).

```text
c-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3419690530281514, "source_id": "e99408d647c7"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "e99408d647c7", "trial_count_per_room_fps": 1}
................................................................................................................................................................
----------------------------------------------------------------------
Ran 160 tests in 3.453s

OK
```

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/implement-change.md
- Project: repo/bots.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting handoff: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Supporting handoff: goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
- Supporting handoff: goals/G-002-final-boss/73-studio-to-gameplay-engineer.md
- Supporting handoff: goals/G-002-final-boss/74-gameplay-engineer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/75-studio-to-gameplay-engineer.md
