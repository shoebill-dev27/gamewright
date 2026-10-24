---
kind: handoff
goal: G-002
seq: 60
from: qa
to: studio
stage: Verify
outcome: fail
---
# 60: qa → studio — ソース照合の追加所見と独立検証の供給不足

## Task

不足しているテスト本文・省略されていないログ・追加実行枠を供給し、独立QAを継続する。ボスbotの観測情報条件について、以下のソース所見を確認して検証経路を整理する。

## Context

59の依頼に従い、packet内の仕様、保存ソース本文、今回の収録実行結果を独立に照合した。実装者の自己評価は根拠にしていない。

今回も実行枠は0回である。Loadに指定されたrepo/tests/の本文はpacketに含まれていない。追加実行、ファイルからのsource_id再算出、完全ログの保存は実施できていない。収録結果の再評価だけで独立検証完了とはしない。

## Findings

### 総合判定

**fail：全基準の独立検証は未完了。加えて、ボスbotの条件付きFPS比較にはソース上の不適合所見がある。**

152 tests成功は今回の収録でも確認できる。ただしテスト本文がないため、条件・操作・assertを基準へ対応付けられない。未確認項目をsuite成功でpassにしていない。

### 識別と証拠の所在

- 保存ソース本文のBUILD：`0.6-g002-public-32`。
- 今回の全収録出力のsource_id：`04fa2b1c168a`。
- 保存ファイルからの独立ハッシュ再算出：未実施。本文と収録出力が同一ソース集合であることは未確定。
- 完全ログ：packetには供給されていない。Round 2 traceとRound 3 botsは明示的に中段が切断されている。

使用した実行証拠は今回の`@run-results`である。

| 参照 | コマンド・入力 | 観測範囲 |
|---|---|---|
| Round 1 tests | `python3 -m unittest discover -s tests` | 152 tests、Exit 0、2.886秒。本文・個別assertなし |
| Round 2 boss-zero-30/60 | `python3 play.py --view trace SCRIPT` | 両FPS。距離0開始、直交移動、driver時刻0.4〜2.4のpause。中段省略 |
| Round 3 retained-and-boss-30/60 | `python3 bots.py SCRIPT` | camper/walker/dodger、rooms 1-5、limit 120、hearts 3,2、log on。中段省略 |
| Round 3 boss-zero-player-60 | `python3 play.py --view player SCRIPT` | 60 FPSの上記距離0診断、view-every 10。表示全文あり |

入力列は各参照のScript欄にある。今回新たに実行したコマンドはない。

### 追加所見：D-019のボスbot観測条件

`repo/bots.py::_dangers`のactive charge分岐は、次の内部値を使う。

```python
e.phase_left * LUNGE_SPEED + 0.6
```

これを危険経路の残長として`_threat`へ渡し、`ahead > length`なら危険候補から外す。したがって、この値は単なるログではなく、回避・停止・その後の行動選択に影響する。

一方、`repo/run_driver.py::Output.emit`のplayer viewは、active中の残時間を表示していない。残時間を表示するのはwarningとrecoveryだけである。botも、表示済み発動時刻を記憶して残時間を算出する経路ではなく、内部`phase_left`を直接読む。

D-019項目6および仕様§8の「player viewで読める情報」「未表示の将来状態を使わない」という比較条件に対し、この判断経路は適合を確認できない。**現状のボスbot比較を条件付きpassにはできない。** 全判断経路を見たとの主張もできないが、この分岐だけで公開情報限定の条件には具体的な問題が残る。

これはゲーム戦闘結果の再現済み不具合とは区別する。対応は試験道具の情報取得経路を整理し、両FPS・開始hearts 3/2を再測定すること。秒数や難度の調整要求ではない。

また、`_hurt_lines`はboss被弾をshot側の診断分岐へ送り、収録にも`source boss`と`shot position not found (fired in this frame)`が併記される。被弾イベントのsourceは読めるが、この補助文から突進の接触位置を証明できない。

### ソースから確認できた事項

- `game.py::ROOMS`の第1〜4部屋は保持仕様の構成・位置・順序と一致する。第5部屋はboss (12,4)だけ。GRUBSと共有定数も提示仕様の値と一致する。
- 境界は`session.py::_enter`で新しいGameを生成する。heartsは入場時に`min(3, old_hearts + 1)`となる。反応記憶の初期化は`run_driver.py::drive`のgeneration変更時に実装されている。
- 同フレームの結果判定は`Game.step`で敵、既発射弾、結果の順。`_resolve_result`は死亡優先で残弾と照準を消す。
- retry時のpending破棄処理は`drive`に存在する。ただし処理の存在と、要求された独立実行証拠は別である。
- D-022の旧room 5注記はlegacy playerだけに置かれ、manualも一致する。
- 公開driverのinterval検証、shot ID採番、消滅理由、summaryの実装経路は読める。ただし全条件の実行確認は未完了。

### 基準別・FPS別判定

「未確認」は部分証拠があっても基準全体を合格にできない場合を含む。

| 基準 | 30 FPS | 60 FPS | 根拠・不足 |
|---|---|---|---|
| R1 | 未確認 | 未確認 | SPLIT_C_PUBLICは通常入力再生の完走を支持。正規敵全撃破・全入場を両viewで対照する完全ログがない |
| R2 | pass（静的） | pass（静的） | ROOMS、GRUBS、共有定数を仕様と照合。FPSによるデータ分岐なし。挙動回帰の判定は下段に分離 |
| R3 | 未確認 | 未確認 | 1/2/3/0 heartsの境界実行なし |
| R4 | 未確認 | 未確認 | 新Game生成と反応初期化は確認。残存全状態を置いた境界前後assertなし |
| R5 | 未確認 | 未確認 | 構造化結果の遷移は各1秒。境界入力破棄・入場同時刻1回適用の独立証拠なし |
| B1 | 未確認 | 未確認 | 初期値・固定交互順はソースにある。各3回・低HPを満たす観測なし |
| B2 | 未確認 | 未確認 | 距離0 charge右固定と移動後の固定方向は収録で確認。short shot距離0など全条件は不足 |
| B3 | 未確認 | 未確認 | ソースは速度8、active 0.3、壁クランプ。毎フレーム位置・壁比較が不足 |
| B4 | 未確認 | 未確認 | 発射速度3・寿命1の実装。60 FPS playerは発射3.633→回復4.633を確認。全消費条件不足 |
| B5 | 未確認 | 未確認 | chargeの直交回避は部分確認。30 FPSは量子化で1.0667 tiles、60 FPSは1 tile。両攻撃の指定条件は不足 |
| B6 | 未確認 | 未確認 | botのdash件数は接触消費の証明にならない |
| B7 | 未確認 | 未確認 | 保護終了を攻撃途中に置く条件と次攻撃の通常命中が未観測 |
| B8 | 未確認 | 未確認 | 全フェーズのswipe前後比較・致死時新発動なしの実行不足 |
| B9 | 未確認 | 未確認 | 60 FPS playerで回復1.2/1.4秒。開始から4回攻撃のassertなし |
| B10 | 未確認 | 未確認 | 帯内外・上端の実軌道と接触距離なし |
| T1 | 未確認 | 未確認 | 残弾を持つ終端とその後2秒比較なし |
| T2 | 未確認 | 未確認 | 同フレーム致死swipe＋致死既発射弾のfixtureなし |
| T3 | 未確認 | 未確認 | 終端待機の集計はあるが、入力を伴う全状態比較なし |
| T4 | 未確認 | 未確認 | 勝利／死亡retry集計あり。完全初期状態比較・旧入力時刻を越える生存試験なし |
| C1 | 未確認 | 未確認 | 同一試行の時間集計は整合。全入場時刻0の完全列なし |
| C2 | 未確認 | 未確認 | warning中pauseは部分確認。dash・保護・clear表示等の全対象比較不足 |
| C3 | 未確認 | 未確認 | driver-limitとoutcomeの分離は観測。game limit同フレーム優先fixture不足 |
| V1 | 未確認 | 未確認 | 60 FPS診断表示は二攻撃・HP・回復・実弾数を確認。通常run終端・retryを含む両FPS対照不足 |
| V2 | 対象外 | 対象外 | D-021の今回範囲。実機対応済みとは判定しない |

Round 2の距離0 chargeは、30 FPSでwarning 0.033333、60 FPSで0.016667、aim (1,0)。60 FPS playerでは発動0.716667、回復1.016667、追跡再開2.216667を確認する。charge回避後にshort shotで被弾しており、試行全体の無傷を示さない。

### D-019保持回帰とbot測定

| 対象 | 30 FPS | 60 FPS | 判定 |
|---|---|---|---|
| combat14 walker側 | room 1で損失3 | room 1で損失3 | 損失下限1は既に充足。ただし独立1〜2の全成績表は省略部分にあり供給不足 |
| combat14 dodger側 | rooms 1/2 clear、損失0/0 | rooms 1/2 clear、損失0/0 | 収録数値上pass |
| combat15 rooms 3/4 | dash 6/7 | dash 6/8 | 収録数値上pass |
| combat16c rooms 1〜4 | 全clear、損失0 | 全clear、損失0 | 収録数値上pass |
| 新boss比較、開始3/2 | 両方clear、損失0 | 両方clear、損失0 | 数値条件は充足。観測情報条件は上記所見によりfail |
| 共有combat1〜11、17〜21 | 未確認 | 未確認 | 個別テスト本文・assert対応なし |
| step68保持部分 | 未確認 | 未確認 | 文字列定義はソース一致。全実行・旧出力比較不足 |
| step72 R3-1〜10保持部分 | 未確認 | 未確認 | R3-1の配置は静的一致。他の条件・assert不足 |
| step94 W1〜8保持部分 | 未確認 | 未確認 | 方向算出・文言はソース一致。W1〜6全ケース・旧出力比較不足 |

独立3/4のcamperは、開始3 hearts、limit 120、同一初期位置・向き。

| FPS・部屋 | 結果 | 終了hearts／損失 | 秒 | 被弾源 | 攻撃／dash |
|---|---|---|---:|---|---|
| 30・3 | death | 0／3 | 6.30 | shot 3 | 0／0 |
| 30・4 | death | 0／3 | 6.73 | shot 3 | 1／0 |
| 60・3 | death | 0／3 | 6.30 | shot 3 | 0／0 |
| 60・4 | death | 0／3 | 6.75 | shot 3 | 1／0 |

独立3/4のwalker成績と判断ログ全文は今回も省略されている。数値を推定しない。camperの行動分岐はソースで読めるが、判断文言をnoteへ記録していないため、実行ログには主に被弾・stunが残る。

cap遅延の一般上限5は、通常静止試験の最大3やsuite greenからは合格にできない。旧第5部屋依存の試験がどこで置換されたかも、tests本文なしでは追跡できない。

### D-022

| 基準 | 30 FPS | 60 FPS | 根拠・不足 |
|---|---|---|---|
| L1 | 未確認 | 未確認 | 注記以外の変更前出力一致・60秒上限実行比較なし |
| L2 | 未確認 | 未確認 | ソースの表示条件は一致。各旧部屋出力未収録 |
| L3 | 未確認 | 未確認 | 指定された同一入力のmode room＋room 5比較なし |
| L4 | pass（文書） | pass（文書） | manualと旧経路注記条件が一致 |
| S1 | 未確認 | 未確認 | 正常命中の発射／消滅抜粋あり。未接触・dash・保護の全列不足 |
| S2 | 未確認 | 未確認 | hit時の1秒維持は部分確認。他の理由不足 |
| S3 | 未確認 | 未確認 | 残弾終端のcleared全列なし |
| S4 | 未確認 | 未確認 | retry後S1と旧removed再発なしの列なし |
| S5 | 未確認 | 未確認 | 60 FPS player診断にID露出なし。全条件・両FPS不足 |
| O1 | 未確認 | 未確認 | 収録カウンタは121/241で上限内。数え方を含むテスト本文なし |
| O2 | 未確認 | 未確認 | 間隔0.5/10のイベント・結果比較なし |
| O3 | 未確認 | 未確認 | 既定実装値は確認。変更前出力比較なし |
| O4 | 未確認 | 未確認 | deathと構造化3 attemptsのsummaryは整合。全終了条件の状態対照不足 |
| O5 | 未確認 | 未確認 | parserの範囲検証は確認。拒否実行出力なし |
| O6 | 未確認 | 未確認 | suiteは1200秒完了を報告。全出力とテスト本文がなく切断なしを独立確認できない |

### 同一試行の時間と後続判断

通常入力再生attempt 1の収録値は次のとおり。独立部屋の時間合算ではない。

| 項目 | 30 FPS | 60 FPS |
|---|---:|---:|
| ラン時刻 | 86.966667秒 | 103.533333秒 |
| 部屋1/2/3/4/5 | 6.633333 / 20.733333 / 15.633333 / 18.333333 / 21.633333秒 | 9.616667 / 25.066667 / 15.016667 / 16.966667 / 32.866667秒 |
| 遷移 | 4回、各1秒 | 4回、各1秒 |
| pause | 2秒 | 2秒 |
| driver経過 | 120秒 | 120秒 |
| 終端待機 | 31.033333秒 | 14.466667秒 |
| boss入場hearts／hurt | 3／0 | 3／0 |
| 攻撃／boss命中／dash | 41／12／34 | 41／12／45 |

部屋時間＋遷移はラン時刻、ラン時刻＋pause＋終端待機はdriver経過に一致する。retryは勝利後と死亡後の2回。attempt 2は自然死亡、attempt 3はunfinishedである。

15〜20分Visionとの差はDesignerへ保持する。人間の体験時間と同一視せず、新たな秒数ゲートは設けない。

### 具体的な供給不足

59が要求する追加実行に対して、packetは最初から0 roundsである。また以下が欠けている。

1. `repo/tests/*.py`全本文。個別テストの条件・assert・対応IDを読むために必要。
2. Round 2/3の省略されていないログと、公開連続入力再生の両FPS・両view完全出力。
3. 保存ソース識別を独立算出し、不足fixtureと公開再生を実行できる枠。
4. L1/O3等の変更前比較に使える基線出力、または比較可能な保存ソース。
5. 完全ログと検証入力を永続参照できる供給経路。今回の許可書込先はhandoff一件だけである。

これは実機ホストやgamepad供給の要求ではない。明確な基準未定義を示す所見もない。今回をpartialとしない理由は、継続に必要な入力・実行枠が具体的に欠けているためである。

## Decisions already made

- D-017：二攻撃、境界、終端、pause・retry・時刻の契約を保持。
- D-019：旧集計を終了し、保持回帰・条件付きbot比較・実測後Designer判断を要求。
- D-021：今回の対象はテキスト・スクリプト方式。実機供給と旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。

## Constraints

- 製品コード・仕様は変更していない。
- 未確認をpassにしない。静的確認、収録実行、fixture、生成入力再生、bot、独立Playを区別する。
- ボスbotの比較条件の所見を、戦闘難度やゲーム本体の再現済み不具合へ拡張しない。
- 新たな難度・秒数ゲートを置かない。
- QA結果・期待値・Review用体験信号を独立Play資料へ転記しない。

## Open questions

1. tests本文、完全ログ、追加実行枠を次の独立QAへ供給できるか。
2. ボスbotのactive残時間参照を、公開情報だけに基づく試験道具としてどう扱うか。整理後の両FPS・hearts 3/2再測定が必要。
3. 変更前一致を要求するL1/O3等について、比較基線を供給できるか。

## Expected output

Studioは供給不足を解消して独立QAを再ルートする。ボスbot所見は試験道具の担当へ渡し、公開情報限定条件を満たす具体的な経路と再測定証拠を用意する。

次のQAは保存source_idを独立算出し、tests本文のassertを基準に対応付け、不足条件を両FPSで実行する。旧未来入力破棄は新attemptが旧入力時刻を越える条件、または破棄列の直接観測で証明する。

全基準合格後に限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewへ進める。本Stepでは合格ルートへ進めない。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/tests/*.py（次Stepでは本文を必ず供給）
- Project: 今回の@run-results、および省略のないログ・入力・基線比較資料
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/59-studio-to-qa.md
