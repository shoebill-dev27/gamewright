---
kind: handoff
goal: G-002
seq: 16
from: technical-director
to: studio
stage: Plan
outcome: question
---
# 16: technical-director → studio — 技術計画とBuild開始前の実行・実機入力依存

## Task

Studioは以下の技術計画と未確認事項を確認し、実行基線の同定とdesktop実機入力の実装・検証環境を確保する。承認範囲を超える費用が必要ならGame Directorへ戻し、開始条件を満たしてからBuildを開く。

## Context

D-015〜D-019により、連続ラン、第5部屋の単体ボス、回復、終端、retry、旧基準の適用変更が確定した。本Stepはtechnical-planに従った静的な技術計画であり、ゲーム変更、独立QA、体験評価は行っていない。

## Findings

### 1. 実行基線と計画の限界

証拠はパケット内の本文だけである。実ファイル、git履歴、Python実行結果は取得していない。指定sha `27fe16268ac8`との一致、既存試験の成功件数、実行時間、難度はすべて未確認。

README、manual、game.py、player bannerは0.6で一致し、project.mdは0.4である。文書更新の遅れの可能性はあるが、shaや履歴の証拠なしに原因を確定しない。Buildの名称と対象commitは別字段で記録する。

Build前の基線確認は次の順序とする。

1. `repo/`のgitルート、対象commit、作業差分の有無、指定shaとの関係を確認する。認証情報や環境変数の値は出力しない。
2. Pythonの版と依存を確認し、`repo/`で `python3 -m unittest discover -s tests` を実行する。失敗を既存／新規で区別できる記録を残す。
3. 既存のplayer／trace、各botの30/60 FPS実行を同一対象で確認する。60秒上限、死亡、クリア後の残弾・操作は静的所見の再現対象とし、未実行の不具合を確定扱いしない。
4. 0.4／0.6表記の由来を確認してStudioへ返す。project.mdはこのStepでは変更しない。

step46、step68、step72、step94の全文とD-011〜D-014はパケットにない。提供仕様が示す保持対象は計画できるが、細目の完全な回帰網羅は確認できない。Build／QAへ正本をロードする必要がある。

### 2. 技術構造

**戦闘とラン進行を分ける。** 既存Gameの部屋戦闘を維持し、その外側にRunSession相当の進行管理を置く。通常ランは `combat / room_clear / won / dead` を持ち、pauseは各状態を凍結する独立フラグとする。独立部屋・practiceは診断モードとして保持し、通常ランのチェックポイントにはしない。

Gameにはフレーム末の結果解決と終端停止を追加する。受理済み行動、存命主体の新規攻撃、既発射弾の接触を解決した後、死亡→勝利／部屋クリアの優先順位で一度だけ確定する。致死スワイプで主体を無効化しても既発射弾を早期削除しない。確定時に残弾・予兆を消し、以後のstepと戦闘入力で戦闘状態を変えない。

部屋入場は単一処理へ集約する。新しいGame相当の状態を正規配置から生成し、生存者のheartsだけを上限3で1回回復する。反応ルール定義・順序はセッション側に保持し、実行時刻、直前盤面、メッセージ記憶を初期化する。retryは同じ初期化経路を使い、新規通常ランとの差を試行番号とセッション設定だけに限定する。

**ボスは専用分岐にする。** Enemyのkind判定、mark、更新、攻撃被害、予兆描画、trace、botsにある「grub以外はspitter」の前提を明示的な種別分岐へ改める。既存grubの通常接触で突進を短縮する処理はボスへ流用しない。ボスは攻撃名、phase、固定照準、残時間、一撃消費を保持する。

弾は発射元・寿命・消滅理由を区別できる表現へ移行する。既存spitterの寿命5秒とボスの寿命1秒、部屋端条件、cap参加条件を混同しない。ボス短射のactive時間は弾の早期消滅から独立させる。接触判定方式・半径・速度は仕様どおり保持する。

### 3. 公開入力・時刻・観測方式

以下は新設する構文案であり、現行で実行可能との主張ではない。Buildでparserとmanualを同時更新する。

| 構文 | 契約 |
|---|---|
| `mode run` | 通常ラン。room指定・practice setupとの併用はエラー |
| `mode room`、`room 1`〜`room 5`／`empty` | 独立診断。既存roomスクリプトはこのモードとして互換維持 |
| `attempt 1`、`attempt 2`… | 時刻指定戦闘入力を試行ごとに区分。retry後は新試行の列だけを使用 |
| `<seconds> move/stop/attack/dash ...` | runではラン時刻、roomでは部屋時刻。同時刻は記載順 |
| `control <driver-seconds> pause/resume/retry` | 停止しない制御用時刻で発火。retryの受理は終端だけ |
| `limit <game-seconds>` | 試行のゲーム時間上限。到達はunfinished |
| `driver-limit <seconds>` | pauseや終端待ちも含む実行制御上限。ゲームの勝敗と別に報告 |

driver時刻はheadlessでは固定刻みで進め、実機では単調増加時計で制御する。ゲーム時刻停止中もresumeを実行できる。C2の外部経過2秒は実機時計でも確認し、headlessの制御刻みだけで実時間確認済みとはしない。

各tickでは制御操作、入場初期化・開始表示、期限入力、反応評価、戦闘step、結果確定の順を明示する。境界中に期限が来た戦闘入力は破棄し、入場時刻一致分だけを初期化後に受理する。pause中の戦闘入力も破棄する。retry時に旧試行の未来入力を廃棄する。

イベントにはbuild識別、試行番号、部屋、ラン時刻、部屋時刻、frame、通番を付ける。状態観測には照準、各残時間、保護、予約攻撃、攻撃消費、弾ID・消滅理由、入力の受理／拒否理由を含める。B3・B10等のためイベント発生時だけでなく毎フレームのtraceを選択可能にする。

player viewは同じ状態から公開観測を生成し、§6の全文言と即時描画契機を実装する。メッセージを先に収集してから反応・表示へ渡し、フレーム内の複数変化や入場による欠落を防ぐ。弾の重なりは活動弾数でも示す。

60秒の暗黙クランプを外し、明示limitで長時間player／traceを実行できるようにする。通常ラン測定はまず1200ゲーム秒を設定し、未完了なら原因を記録して必要長を再評価する。1200秒到達を合格や死亡にしない。出力は逐次保存し、長時間traceのメモリ増加を避ける。

### 4. 実機入力の不足と費用

提供ビルドには実機keyboard／gamepad経路がない。V2にはdesktopで動く薄い入力・表示ホストの新設が必要である。候補はSDL系の入力層を使う最小ホストとし、ゲームルールは共通Sessionへ渡す。具体ライブラリは対象OS、既存依存、利用可能な機器を確認して選ぶ。グラフィカル素材制作は含めない。

移動、attack、dash、pause、終端retryを共通actionへ正規化する。ボタン・軸の押下／解放を記録し、入場・retry後は保持中の入力を解放まで遮断する。pause突入では保持移動を解除し、予約攻撃は凍結する。アダプタの模擬試験に加え、実機両入力でV2を独立確認する。

実機環境・依存導入・表示ホストの実現費用は未確定であり、headless完了後の任意課題にはしない。必要なホストが承認案Aを実質的に超える場合は実装前にGame Directorへ戻す。

### 5. 実装順序・依存・工数

小規模な既存Python実装を前提とした暫定見積もり。実行基線未確認のため確約ではない。

| 順 | 作業・変更対象 | 依存 | 人日目安 |
|---|---|---|---|
| 0 | sha・既存実行基線、欠けた回帰正本、実機環境・依存の同定 | Studioの環境供給 | 0.5〜1 |
| 1 | Gameの結果解決・終端停止、観測字段、共有回帰 | 0 | 1〜2 |
| 2 | boss種別・二攻撃・弾の属性と消費、B試験 | 1 | 2〜3 |
| 3 | Session、境界回復、両時刻、pause、retry、入力列 | 1、2との契約固定 | 2〜3 |
| 4 | play parser、公開観測、即時表示、長時間trace、manual／README | 2、3 | 1.5〜2.5 |
| 5 | 対応bots、報告・同一試行計測、旧assert移行 | 2〜4 | 1.5〜2.5 |
| 6 | desktop実機ホスト、保持入力解除、操作記録 | 0、3、4 | 2〜4 |
| 7 | 統合確認、両FPS基線、独立検証用資料 | 1〜6 | 1〜2 |

Build準備から統合まで約11.5〜20人日。独立QA 2〜3人日、限定Art確認0.5〜1人日、独立Play 1〜2人日を別枠とする。Designerの実測後判断、修正・再検証の日数は所見次第である。予算上限はパケットにないため、この見積もりが承認済み費用内とは断定できない。

コード実装は逐次とする。Game、play、botsが敵種別・イベント・時刻の共有契約に依存し、並行変更の統合リスクが利益を上回る。独立QA・Art・Playは所定順序を保持し、実装担当が自己承認しない。

### 6. 受け入れ基準と試験対応

全自動シナリオを30/60 FPSで分け、player表示と同じビルドの状態観測を対照する。

| 対象 | 自動化と独立確認 |
|---|---|
| B1 | 正規5番の位置・HP・単体構成、HP低下前後を含む各3回以上の攻撃順 |
| B2 | 予兆中移動、距離0、固定方向、0.7／0.8秒の予兆と即時表示 |
| B3 | 開放位置・壁の毎フレーム軌道、全active時間、回復開始 |
| B4 | 未接触・通常命中・保護吸収・寿命到達・部屋端で弾数、消滅理由、固定active時間 |
| B5 | 各予兆から0.4秒以内の直交1 tile移動と無傷 |
| B6・B7 | 各攻撃への実接触、dash／被弾保護、消費、保護終了後無傷、次攻撃の通常命中 |
| B8 | 全phaseで非致死swipe前後比較、予兆継続文言、致死時の新接触・発射停止 |
| B9 | 回復中接触、射程と向きを整えた4回の攻撃、1.2／1.4秒 |
| B10 | 弾0.39以下・0.40超・帯内・0.40、突進0.57以下・0.60超・帯内・0.60を軌道と距離で判定 |
| R1・R2 | 正規配置で実際に撃破する通常ランと、1〜4のデータ・共有パラメータ回帰。状態設定による通過は禁止 |
| R3・R4 | hearts0/1/2/3と残存状態を独立fixtureで作り、回復1回と全リセット字段・次の行動を比較 |
| R5・C1 | 境界1秒、両時刻、期限切れ／入場同時刻入力、保持入力・反応記憶初期化 |
| T1〜T4 | 残弾クリア、同フレーム相打ち、終端2秒凍結、勝利／死亡retryと新規初期状態の一致 |
| C2 | 予兆・dash・保護・境界でpause、2秒後resume。予約攻撃保持、戦闘入力破棄も確認 |
| C3 | unfinishedと勝敗を別字段にし、limit同フレームの死亡／勝利／クリアを先に記録 |
| V1 | §6の常設情報・全メッセージ・描画時刻・重なりをQAが対照。限定Art確認へplayer出力を渡す |
| V2 | keyboard／gamepadの実機操作記録と同等状態遷移。模擬入力だけでは合格にしない |

時間許容は各FPSの1フレーム以内。接触帯は命中・消費の差だけに適用し、フェーズ・照準・表示の差を免責しない。

### 7. 旧assertと共有回帰の移行

Buildは「旧assert→保持／終了→新試験ID」の対応表を変更報告へ付ける。

- `test_rooms_match_the_spec`：1〜4を保持・不足する1番確認を補い、旧5番brute位置を新5番B1へ置換する。
- CueGapTest：4番の実部屋、強制同時射撃、cap遅延、cue取消とpractice既定offsetを保持する。旧5番部分はB2／B4へ接続し、空ループによるgreenを防ぐ。
- SpitterTest room3の静止12秒・最大3は条件付き回帰として保持する。D-007のcap遅延・一般上限5は別試験で確認する。
- BotsTestの旧13下限、clear数、比率、camper比較、旧5番dash数を終了する。14の1〜2、15の3・4、独立1〜4のdodger FPS比較を保持する。
- 新5番は開始hearts3／2を分けた対応dodger比較とB5／B6へ置換する。旧総計を新ランの集計に読み替えない。
- bot終了、ログ有無の結果一致、判断ログ、walker比較距離、brute方針を保持し、新5番でもログが結果を変えないことを確認する。
- combat基準1〜11、17〜21、step68のvariantとrunner kill、step72 R3-1〜R3-10、step94 W1〜W8を追跡する。旧5番spitter表示経路は4番・practiceへ移し、ボス短射表示を別確認する。
- 旧5番fixtureは標準成果に含めない。必要時だけ共有回帰専用と明記する。過去Decision・G-001結果は編集しない。

### 8. bot・通常ラン計測と返却経路

対応dodgerは公開観測のB、攻撃名、固定方向・範囲、phase、弾を使う専用方針を追加し、独立1〜4の方針を維持する。0.15秒反応を共通にし、将来の非公開状態や予兆中断を利用しない。QAは情報入力と実判断ログを確認する。

独立3・4は各bot×各FPSで開始hearts、clear／death／unfinished、終了hearts、損失、秒数、被弾源、attack／dash数、limit、方針・build識別を報告する。合計ゲートは作らない。3・4のdodger dash0回はDesignerへ返し、使用を強制する調整をしない。

新5番は同一build・方針・位置・向き・戦闘状態・limitで、hearts3開始と2開始をそれぞれ30/60比較する。同じclear結果、損失差1以下を確認する。一方だけunfinishedなら比較未完了。両方死亡／unfinishedでも攻略可能性は未証明とする。差は判断時刻・位置・照準・距離・消費・被弾で診断し、帯内由来でも閾値超過はDesignerへ戻す。帯外や規則の差はQA不合格とする。

通常ランは新規起動から実際の正規敵撃破を通した試行を記録する。各試行でラン時刻、pauseを分離した実経過、部屋別時間、遷移、ボス初入場hearts、被弾、回復中の反撃、retry回数、到達・終端を対応付ける。完走・死亡・未完了を分け、試行数を明示する。独立部屋時間の合算は禁止する。加速headlessの処理時間を人間のプレイ時間と呼ばない。

返却順序は次のとおり。

1. Build統合後：対応bot確認、両FPS基線、通常到達の初回証拠。明白な対処不能・到達不能はPlay前にDesignerへ返す。
2. 独立QA：固定build、実行手順、入力script、境界fixture、期待する仕様ID、観測方法と未実施項目を渡す。
3. 限定Art Verify：player出力で二攻撃、予兆／実弾、回復／次攻撃、HP、重なり、終端／retryの識別を確認する。
4. 独立Play：Studioが通常起動・操作・記録方法だけを渡す。実装説明、設計の期待結果、Review用体験信号は渡さない。
5. QA・Art・Play後、Review前：Designerへ全測定条件・件数・ログ・未検証事項を戻す。追加数値ゲートと調整の要否、不要なら理由をDecision／仕様へ記録する。
6. 15〜20分との差があれば原因を報告する。HPや待機による時間合わせをせず、範囲内で解消不能ならGame Director経由でOwnerへ戻す。

### 9. Build開始判断

戦闘・進行の仕様に、静的に明らかな実現不能は認めない。追加難度ゲートの未設定はD-019が意図した実測後判断であり、それ自体は開始阻害ではない。

ただし、指定sha・実行基線、欠けた回帰正本、実機ホストと検証環境・費用が未確認である。本StepではPlanを無条件完了とせず、Build開始を保留してStudioへ返す。上記を確認し費用が承認範囲内と整理できれば、数値仕様を変更せずBuildへ進める。範囲超過なら先にDecideへ戻す。

## Decisions already made

- D-001：attackとdashの戦闘入力を保持する。
- D-002／D-003：既存接触方式と帯。ボスへの限定適用はD-017による。
- D-004／D-005／D-007：既存敵の非中断、gap、保護中消費、room3の一般境界を保持する。
- D-015／D-016：連続ラン、第5部屋単体ボス、先頭retryと体験方向。
- D-017：ボス、回復、終端、時刻・入力・表示の契約。
- D-018／D-019：旧集計の適用終了、保持回帰、対応bot比較とDesigner実測後判断。
- 新規Decisionは作成していない。技術方式は上記計画として提示した。

## Constraints

第1〜4部屋と共有戦闘ルールを維持する。新戦闘入力、チェックポイント、全面改修、時間合わせだけのHP増加・待機を追加しない。

実行未確認を成功と扱わず、headlessをV2の代用にしない。Technical Directorは難度数値を変更せず、自身の計画結果をQA承認しない。

このHandoffはStudio向けである。Playtesterには設計・実装情報を除いた別資料を作成する。秘密情報、個人情報を実行記録・後続資料へ含めない。

## Open questions

1. Studio：指定shaの実行可能なrepo、Python、欠けた回帰正本を供給し、基線確認をどのStepで完了するか。
2. Studio：対象desktop OS、keyboard／gamepad機器、入力・表示ホストの依存導入と独立実機検証環境を確保できるか。
3. Studio／Game Director：暫定Build費用11.5〜20人日と独立検証枠は承認案Aの範囲内か。実機ホストが超過する場合は実装前に判断へ戻す。
4. Designerへの仕様質問は現時点でない。実測後の追加ゲート・調整判断は未実施であり、Review前に必須とする。

## Expected output

Studioは実行基線・実機入力環境・費用の未確認事項を解決する経路を確定し、Plan完了とBuild開始可否を記録する。超過が具体化した場合はGame Directorへ戻す。

Buildを開く際は本計画の依存順、全試験ID、旧assert対応、同一試行計測、未確認事項をGameplay Engineerへ渡す。その後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/15-studio-to-technical-director.md
